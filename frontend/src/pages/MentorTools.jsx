import React, { useState } from 'react';
import { FileUp, UploadCloud, BookOpen, CheckCircle, AlertCircle } from 'lucide-react';
import api from '../services/api';

const MentorTools = () => {
    // PDF Module State
    const [pdfFile, setPdfFile] = useState(null);
    const [moduleName, setModuleName] = useState('');
    const [moduleLevel, setModuleLevel] = useState('beginner');
    const [uploading, setUploading] = useState(false);
    const [pdfResult, setPdfResult] = useState(null);

    // Challenge Upload State
    const [challengeFile, setChallengeFile] = useState(null);
    const [challengeUploading, setChallengeUploading] = useState(false);
    const [challengeResult, setChallengeResult] = useState(null);

    const handlePdfUpload = async (e) => {
        e.preventDefault();
        if (!pdfFile) return;

        const formData = new FormData();
        formData.append('file', pdfFile);
        formData.append('level', moduleLevel);
        formData.append('module_name', moduleName || 'Custom Module');

        setUploading(true);
        setPdfResult(null);
        try {
            const response = await api.uploadPdfModule(formData);
            setPdfResult({ 
                success: true, 
                message: `Successfully parsed ${response.data.questions_parsed} questions!` 
            });
            setPdfFile(null);
            setModuleName('');
        } catch (err) {
            setPdfResult({ 
                success: false, 
                message: err.response?.data?.detail || err.message 
            });
        } finally {
            setUploading(false);
        }
    };

    const handleChallengeUpload = async (e) => {
        e.preventDefault();
        if (!challengeFile) return;

        const formData = new FormData();
        formData.append('file', challengeFile);

        setChallengeUploading(true);
        setChallengeResult(null);
        try {
            const response = await api.uploadChallenges(formData);
            setChallengeResult({ 
                success: true, 
                message: `Successfully uploaded ${response.data.challenges_created} challenges!` 
            });
            setChallengeFile(null);
        } catch (err) {
            setChallengeResult({ 
                success: false, 
                message: err.response?.data?.detail || err.message 
            });
        } finally {
            setChallengeUploading(false);
        }
    };

    return (
        <div className="container mx-auto px-4 py-12">
            <div className="mb-12">
                <h1 className="text-4xl font-bold text-slate-800 dark:text-slate-100">
                    Mentor Tools
                </h1>
                <p className="text-slate-600 dark:text-slate-400 mt-2">
                    Create modules from PDFs and upload challenge tracks for your students.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* PDF to Module Section */}
                <div className="glass-card p-8">
                    <div className="flex items-center mb-6">
                        <FileUp className="text-blue-600 mr-3" size={28} />
                        <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                            Create Module from PDF
                        </h2>
                    </div>
                    <p className="text-slate-600 dark:text-slate-400 mb-6">
                        Upload a PDF with questions in <code className="bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-sm">Q: [Question] A: [Answer]</code> format.
                    </p>

                    <form onSubmit={handlePdfUpload} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                Module Name
                            </label>
                            <input
                                type="text"
                                value={moduleName}
                                onChange={(e) => setModuleName(e.target.value)}
                                placeholder="e.g., Python Basics"
                                className="input-field w-full"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                Difficulty Level
                            </label>
                            <select
                                value={moduleLevel}
                                onChange={(e) => setModuleLevel(e.target.value)}
                                className="input-field w-full"
                            >
                                <option value="beginner">Beginner</option>
                                <option value="intermediate">Intermediate</option>
                                <option value="expert">Expert</option>
                            </select>
                        </div>

                        <div className="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-xl p-8 text-center bg-slate-50/50 dark:bg-slate-900/50 hover:border-blue-400 dark:hover:border-blue-600 transition-colors">
                            <input
                                type="file"
                                accept=".pdf"
                                onChange={(e) => setPdfFile(e.target.files[0])}
                                className="hidden"
                                id="pdf-upload"
                            />
                            <label htmlFor="pdf-upload" className="cursor-pointer">
                                <UploadCloud className="mx-auto mb-4 text-slate-400" size={48} />
                                <p className="text-lg font-medium text-slate-700 dark:text-slate-300">
                                    {pdfFile ? pdfFile.name : "Click to choose a PDF file"}
                                </p>
                                <p className="text-sm text-slate-400 mt-2">Max file size: 10MB</p>
                            </label>
                        </div>

                        {pdfResult && (
                            <div className={`flex items-center gap-2 p-4 rounded-lg ${
                                pdfResult.success 
                                    ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' 
                                    : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                            }`}>
                                {pdfResult.success ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
                                {pdfResult.message}
                            </div>
                        )}

                        <button
                            type="submit"
                            className="btn-primary w-full"
                            disabled={uploading || !pdfFile}
                        >
                            {uploading ? "Processing PDF..." : "Generate Module"}
                        </button>
                    </form>
                </div>

                {/* Challenge Upload Section */}
                <div className="glass-card p-8">
                    <div className="flex items-center mb-6">
                        <BookOpen className="text-purple-600 mr-3" size={28} />
                        <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                            Upload 30-Day Challenges
                        </h2>
                    </div>
                    <p className="text-slate-600 dark:text-slate-400 mb-6">
                        Upload a JSON or CSV file with daily challenges to create a learning track.
                    </p>

                    <form onSubmit={handleChallengeUpload} className="space-y-6">
                        <div className="bg-slate-100 dark:bg-slate-800/50 rounded-lg p-4">
                            <h3 className="font-medium text-slate-700 dark:text-slate-300 mb-2">Expected Format (JSON):</h3>
                            <pre className="text-xs text-slate-600 dark:text-slate-400 overflow-x-auto">
{`[
  {
    "title": "Day 1: Variables",
    "question": "What is x?",
    "category": "Coding",
    "answer": "10"
  },
  ...
]`}
                            </pre>
                        </div>

                        <div className="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-xl p-8 text-center bg-slate-50/50 dark:bg-slate-900/50 hover:border-purple-400 dark:hover:border-purple-600 transition-colors">
                            <input
                                type="file"
                                accept=".json,.csv"
                                onChange={(e) => setChallengeFile(e.target.files[0])}
                                className="hidden"
                                id="challenge-upload"
                            />
                            <label htmlFor="challenge-upload" className="cursor-pointer">
                                <UploadCloud className="mx-auto mb-4 text-slate-400" size={48} />
                                <p className="text-lg font-medium text-slate-700 dark:text-slate-300">
                                    {challengeFile ? challengeFile.name : "Click to choose a file"}
                                </p>
                                <p className="text-sm text-slate-400 mt-2">Accepted: .json, .csv</p>
                            </label>
                        </div>

                        {challengeResult && (
                            <div className={`flex items-center gap-2 p-4 rounded-lg ${
                                challengeResult.success 
                                    ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' 
                                    : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                            }`}>
                                {challengeResult.success ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
                                {challengeResult.message}
                            </div>
                        )}

                        <button
                            type="submit"
                            className="btn-primary w-full bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800"
                            disabled={challengeUploading || !challengeFile}
                        >
                            {challengeUploading ? "Uploading Challenges..." : "Upload Challenges"}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default MentorTools;
