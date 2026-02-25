import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Shield, TrendingUp, Users, UserCheck, Copy } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const AdminDashboard = () => {
    const { user, loading: authLoading } = useAuth();
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await api.getAdminStats();
                setStats(response.data);
            } catch (err) {
                console.error("Error fetching admin stats:", err);
            } finally {
                setLoading(false);
            }
        };
        if (user && user.role?.toLowerCase() === 'admin') {
            fetchStats();
        }
    }, [user]);

    const copyToClipboard = (text) => {
        if (!text) return;
        navigator.clipboard.writeText(text);
        alert("Join code copied to clipboard!");
    };

    if (authLoading) {
        return (
            <div className="text-center py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
                <p className="mt-4 text-slate-500">Securing connection...</p>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-12">
            <div className="flex flex-col md:flex-row md:items-center justify-between mb-12 gap-6">
                <h1 className="text-4xl font-bold text-slate-800 dark:text-slate-100 flex items-center">
                    <Shield className="mr-4 text-red-600" size={40} />
                    Admin Command Center
                </h1>

                <div className="flex flex-col md:flex-row gap-4 items-stretch">
                    {/* Admin Profile Details */}
                    <div className="glass-card px-6 py-4 flex items-center border-l-4 border-l-indigo-600 min-w-[280px]">
                        <div className="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center mr-4">
                            <Shield className="text-indigo-600" size={20} />
                        </div>
                        <div>
                            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Admin Profile</p>
                            <p className="text-lg font-bold text-slate-800 dark:text-slate-100">{user?.username}</p>
                            <p className="text-xs text-slate-500">{user?.email}</p>
                        </div>
                    </div>

                    {/* Join Code Card */}
                    {user?.join_code && (
                        <div className="glass-card px-6 py-4 flex items-center justify-between border-l-4 border-l-red-600 min-w-[280px]">
                            <div>
                                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Your Admin Join Code</p>
                                <p className="text-2xl font-mono font-bold text-red-600">{user.join_code}</p>
                            </div>
                            <button
                                onClick={() => copyToClipboard(user.join_code)}
                                className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors text-slate-500"
                                title="Copy Code"
                            >
                                <Copy size={20} />
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {loading ? (
                <div className="text-center py-20">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
                    <p className="mt-4 text-slate-500">Retrieving intelligence...</p>
                </div>
            ) : stats ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                    {/* Stat Cards */}
                    <div className="glass-card p-6 border-b-4 border-b-blue-600">
                        <div className="flex justify-between items-start mb-4">
                            <UserCheck className="text-blue-600" size={24} />
                            <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">Mentors</span>
                        </div>
                        <p className="text-4xl font-extrabold">{stats.mentor_count}</p>
                        <p className="text-slate-500 text-sm mt-1">Under your command</p>
                    </div>

                    <div className="glass-card p-6 border-b-4 border-b-purple-600">
                        <div className="flex justify-between items-start mb-4">
                            <Users className="text-purple-600" size={24} />
                            <span className="text-xs font-bold text-purple-600 uppercase tracking-wider">Students</span>
                        </div>
                        <p className="text-4xl font-extrabold">{stats.student_count}</p>
                        <p className="text-slate-500 text-sm mt-1">Total active learners</p>
                    </div>

                    <div className="glass-card p-6 border-b-4 border-b-amber-500">
                        <div className="flex justify-between items-start mb-4">
                            <TrendingUp className="text-amber-500" size={24} />
                            <span className="text-xs font-bold text-amber-500 uppercase tracking-wider">Total XP</span>
                        </div>
                        <p className="text-4xl font-extrabold">{stats.total_xp.toLocaleString()}</p>
                        <p className="text-slate-500 text-sm mt-1">Points generated</p>
                    </div>

                    <div className="glass-card p-6 border-b-4 border-b-emerald-600">
                        <div className="flex justify-between items-start mb-4">
                            <span className="text-2xl">🔥</span>
                            <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">Avg Streak</span>
                        </div>
                        <p className="text-4xl font-extrabold">{stats.average_streak.toFixed(1)}</p>
                        <p className="text-slate-500 text-sm mt-1">Days of consistency</p>
                    </div>
                </div>
            ) : (
                <p>No stats available.</p>
            )}

            <div className="glass-card p-8">
                <h2 className="text-2xl font-bold mb-6 flex items-center">
                    <Users className="mr-3 text-purple-600" size={24} />
                    Detailed Student Activity
                </h2>

                {stats?.students && stats.students.length > 0 ? (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead className="border-b border-slate-200 dark:border-slate-700">
                                <tr>
                                    <th className="py-4 px-4 font-bold text-slate-500 uppercase text-xs">Student</th>
                                    <th className="py-4 px-4 font-bold text-slate-500 uppercase text-xs">Assigned Mentor</th>
                                    <th className="py-4 px-4 font-bold text-slate-500 uppercase text-xs">Experience</th>
                                    <th className="py-4 px-4 font-bold text-slate-500 uppercase text-xs">Streak</th>
                                </tr>
                            </thead>
                            <tbody>
                                {stats.students.map((student) => (
                                    <tr key={student.id} className="border-b border-slate-100 dark:border-slate-800/50 hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">
                                        <td className="py-4 px-4">
                                            <div className="font-bold">{student.username}</div>
                                            <div className="text-xs text-slate-500">{student.email}</div>
                                        </td>
                                        <td className="py-4 px-4">
                                            <span className="px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-bold">
                                                {student.mentor_name}
                                            </span>
                                        </td>
                                        <td className="py-4 px-4">
                                            <span className="font-mono font-bold text-amber-600">{student.xp.toLocaleString()} XP</span>
                                        </td>
                                        <td className="py-4 px-4">
                                            <span className="font-bold text-emerald-600">🔥 {student.streak}</span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <div className="bg-slate-100/50 dark:bg-slate-900/50 p-12 text-center rounded-2xl border-2 border-dashed border-slate-300 dark:border-slate-700">
                        <p className="text-slate-500 italic">No operational data available for assigned mentors.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdminDashboard;
