import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Megaphone, Calendar } from 'lucide-react';

const AnnouncementList = () => {
    const [announcements, setAnnouncements] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnnouncements = async () => {
            try {
                const response = await api.getAnnouncements();
                setAnnouncements(response.data);
            } catch (err) {
                console.error("Error fetching announcements:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchAnnouncements();
    }, []);

    if (loading) return null;
    if (announcements.length === 0) return null;

    return (
        <div className="mb-12">
            <h2 className="text-2xl font-bold text-slate-700 dark:text-slate-200 mb-6 flex items-center">
                <Megaphone className="mr-2 text-purple-600" size={24} />
                Announcements
            </h2>
            <div className="space-y-4">
                {announcements.map((announcement) => (
                    <div key={announcement.id} className="glass-card p-6 border-l-4 border-l-purple-600">
                        <div className="flex justify-between items-start mb-2">
                            <span className="text-sm font-medium text-slate-500 flex items-center">
                                <Calendar size={14} className="mr-1" />
                                {new Date(announcement.timestamp).toLocaleDateString()}
                            </span>
                        </div>
                        <p className="text-slate-700 dark:text-slate-300 text-lg leading-relaxed">
                            {announcement.content}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AnnouncementList;
