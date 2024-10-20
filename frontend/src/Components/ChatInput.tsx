// ChatInput.tsx
'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from "@/Components/ui/button"
import { Textarea } from "@/Components/ui/textarea"
import { Send } from 'lucide-react'

interface ChatInputProps {
    query: string;
    setQuery: (query: string) => void;
    handleRunQuery: () => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ query, setQuery, handleRunQuery }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className=" w-full max-w-3xl bg-white p-4 shadow-md rounded-lg"
        >
            <div className="max-h-44">
                <div className="p-4">
                    <Textarea
                        placeholder="Explain this database"
                        className="w-full mb-4 p-2 border border-gray-200 rounded-md"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                        <Button
                            onClick={handleRunQuery}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center"
                        >
                            <Send className="w-4 h-4 mr-2" />
                            Run Query
                        </Button>
                    </motion.div>
                </div>
            </div>
        </motion.div>
    )
}

export default ChatInput
