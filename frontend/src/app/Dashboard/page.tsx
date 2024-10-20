'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from "@/Components/ui/button"
import { Textarea } from "@/Components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/Components/ui/card"
import { Send } from 'lucide-react'
import ReactMarkdown from 'react-markdown';
import { } from 'ldrs';


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
    const [response, setResponse] = useState('')
    const [isLoading, setLoading] = useState(false)

    const handleRunQuery = async () => {
        setLoading(true);
        try {
            const res = await fetch('http://localhost:8000/endpoint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            })
            const data = await res.json()
            console.log(data.status)

            if (data.status == 'successful') {
                console.log('IT IS SUCCESSFUL');
                setResponse(data["agent_response"]);
            } else {
                console.log('NAHHH');
                setResponse(`Error: ${data.error}`);
            }

        } catch (error) {
            console.error('Error running query:', error)
            setResponse('Error: Something went wrong')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-ThemeBg p-8 flex flex-col items-center overflow-scroll relative">
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
                <Card className="shadow-lg min-h-[calc(100vh-30vh)] max-h-[calc(100vh-45vh)] mb-2 overflow-y-scroll"> {/* Adjusted min height */}
                    <CardContent className="p-6 h-full overflow-y-auto">
                        {isLoading ? (
                            <div className='w-full h-full flex items-center justify-center'>
                                <l-spiral></l-spiral>
                            </div>
                        ) : (
                            <div className="w-full h-full bg-white rounded-lg flex items-center justify-center text-gray-400 overflow-auto">
                                {response ? (
                                    <ReactMarkdown className="bg-white prose">{response}</ReactMarkdown>
                                ) : (
                                    'How can I help you?'
                                )}
                            </div>)}
                    </CardContent>
                </Card>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="w-full max-w-3xl mt-4 mb-8 fixed bottom-0 transform rounded-lg "

            >
                <Card className="shadow-md overflow-hidden">
                    <CardContent className="flex flex-row p-4">
                        <Textarea
                            placeholder=" E.g. Explain this database"
                            className="w-full bottom-0 min-h-[20px] max-h-10 mr-3 left-1/2 p-2 border border-gray-200 rounded-md"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                            <Button
                                onClick={handleRunQuery}
                                className="bg-blue-600 hover:bg-blue-700 text-white px-4 rounded-md flex items-center"
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