'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from "@/Components/ui/button"
import { Textarea } from "@/Components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/Components/ui/card"
import { Send } from 'lucide-react'

interface FloatingCircleProps {
    size: string;
    initialPosition: { top?: string; left?: string; right?: string; bottom?: string };
    duration: number;
}

const FloatingCircle: React.FC<FloatingCircleProps> = ({ size, initialPosition, duration }) => (
    <motion.div
        className={`absolute rounded-full bg-CircleColor opacity-20 ${size}`}
        initial={initialPosition}
        animate={{
            x: [0, Math.random() * 100 - 50, 0],
            y: [0, Math.random() * 100 - 50, 0],
        }}
        transition={{
            repeat: Infinity,
            duration: duration,
            ease: "easeInOut",
        }}
    />
)

export default function DatabaseVisualizer() {
    const [query, setQuery] = useState('')

    const handleRunQuery = () => {
        console.log('Running query:', query)
    }

    return (
        <div className="min-h-screen bg-ThemeBg p-8 flex flex-col items-center overflow-hidden relative">
            {/* Floating circles */}
            <FloatingCircle size="w-16 h-16" initialPosition={{ top: "10%", left: "10%" }} duration={7} />
            <FloatingCircle size="w-24 h-24" initialPosition={{ top: "20%", right: "15%" }} duration={9} />
            <FloatingCircle size="w-20 h-20" initialPosition={{ bottom: "15%", left: "20%" }} duration={8} />
            <FloatingCircle size="w-32 h-32" initialPosition={{ bottom: "10%", right: "10%" }} duration={10} />

            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="text-3xl font-bold text-blue-800 mb-2 relative z-10"
            >
                Databae.
            </motion.h1>
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-3xl relative z-0"
            >
                <Card className="shadow-lg overflow-hidden">
                    <CardContent className="p-6 h-96">
                        <div className="w-full h-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
                            response will appear here
                        </div>
                    </CardContent>
                </Card>
            </motion.div>
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="w-full max-w-3xl mt-2 relative z-10"
            >
                <h2 className="text-xl font-semibold text-blue-800 mb-2">How can I help you?</h2>
                <Card className="shadow-md overflow-hidden">
                    <CardContent className="p-4">
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
                    </CardContent>
                </Card>
            </motion.div>
        </div>
    )
}