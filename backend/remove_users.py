#!/usr/bin/env python3
"""
Utility script to remove users by username from the SkillSprint database.

Usage:
  Activate your virtualenv, then run from the repo root:

    python backend/remove_users.py --usernames lalith_sai-123 superadmin star_student --yes

If --yes is not provided the script will ask for confirmation before deleting.

The script removes related records in `submissions`, `user_challenges`, and `module_progress`
before deleting the user to avoid foreign-key constraint errors.
"""
import os
import sys
import argparse

# Ensure 'app' package is importable when run from repo root
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from app import models
from app.database import SessionLocal


def remove_users(usernames, assume_yes=False):
    db = SessionLocal()
    try:
        for username in usernames:
            user = db.query(models.User).filter(models.User.username == username).first()
            if not user:
                print(f"User not found: {username}")
                continue

            print(f"Found user: {username} (id={user.id}). Deleting related records...")

            # Delete submissions
            subs_deleted = db.query(models.Submission).filter(models.Submission.user_id == user.id).delete(synchronize_session=False)
            # Delete module progress
            mp_deleted = db.query(models.ModuleProgress).filter(models.ModuleProgress.user_id == user.id).delete(synchronize_session=False)
            # Delete user_challenges entries
            uc_deleted = db.query(models.UserChallenge).filter(models.UserChallenge.user_id == user.id).delete(synchronize_session=False)

            print(f"  Deleted {subs_deleted} submissions, {mp_deleted} module_progress, {uc_deleted} user_challenges")

            # Finally delete the user
            db.delete(user)
            db.commit()
            print(f"  Deleted user: {username}\n")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Remove users by username from SkillSprint DB")
    parser.add_argument("--usernames", nargs="+", help="List of usernames to delete", required=True)
    parser.add_argument("--yes", action="store_true", help="Do not prompt for confirmation")
    args = parser.parse_args()

    print("Users to remove:")
    for u in args.usernames:
        print("  -", u)

    if not args.yes:
        resp = input("Type DELETE to confirm: ")
        if resp.strip() != "DELETE":
            print("Aborted -- confirmation not received.")
            sys.exit(1)

    remove_users(args.usernames, assume_yes=args.yes)


if __name__ == "__main__":
    main()
