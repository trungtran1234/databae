"use client"

import React from "react"
import { motion } from "framer-motion"

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.2,
            delayChildren: 0.3,
        },
    },
}

const itemVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
        opacity: 1,
        scale: 1,
        transition: {
            duration: 0.8,
            ease: [0.6, -0.05, 0.01, 0.99],
        },
    },
}

export default function EnhancedAnimatedBackground() {
    return (
        <motion.div
            className="fixed inset-0 w-full h-full bg-blue-50 overflow-hidden"
            initial="hidden"
            animate="visible"
            variants={containerVariants}
        >
            <svg
                viewBox="0 0 1000 1000"
                xmlns="http://www.w3.org/2000/svg"
                className="w-full h-full"
                preserveAspectRatio="xMidYMid slice"
            >
                {/* Background gradient */}
                <defs>
                    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style={{ stopColor: "#2e2e2e", stopOpacity: 1 }} />
                        <stop offset="100%" style={{ stopColor: "#3d3d3d", stopOpacity: 1 }} />
                    </linearGradient>
                </defs>
                <motion.rect x="0" y="0" width="100%" height="100%" fill="url(#grad1)" variants={itemVariants} />

                {/* Animated circles */}
                <motion.circle
                    cx="10%"
                    cy="10%"
                    r="50"
                    fill="#93c5fd"
                    variants={itemVariants}
                    animate={{
                        scale: [1, 1.2, 1],
                        transition: { repeat: Infinity, duration: 8, ease: "easeInOut" },
                    }}
                />
                <motion.circle
                    cx="90%"
                    cy="90%"
                    r="70"
                    fill="#60a5fa"
                    variants={itemVariants}
                    animate={{
                        scale: [1, 1.3, 1],
                        transition: { repeat: Infinity, duration: 10, ease: "easeInOut" },
                    }}
                />

                {/* Animated paths */}
                <motion.path
                    d="M0,300 Q250,50 500,300 T1000,300 L1000,0 L0,0 Z"
                    fill="#1f1f1f"
                    variants={itemVariants}
                    animate={{
                        d: [
                            "M0,300 Q250,50 500,300 T1000,300 L1000,0 L0,0 Z",
                            "M0,300 Q250,200 500,300 T1000,300 L1000,0 L0,0 Z",
                            "M0,300 Q250,50 500,300 T1000,300 L1000,0 L0,0 Z",
                        ],
                        transition: { repeat: Infinity, duration: 20, ease: "easeInOut" },
                    }}
                />
                <motion.path
                    d="M0,600 Q250,450 500,600 T1000,600 L1000,1000 L0,1000 Z"
                    fill="#1a1919"
                    variants={itemVariants}
                    animate={{
                        d: [
                            "M0,600 Q250,450 500,600 T1000,600 L1000,1000 L0,1000 Z",
                            "M0,600 Q250,750 500,600 T1000,600 L1000,1000 L0,1000 Z",
                            "M0,600 Q250,450 500,600 T1000,600 L1000,1000 L0,1000 Z",
                        ],
                        transition: { repeat: Infinity, duration: 25, ease: "easeInOut" },
                    }}
                />

                {/* Floating shapes */}
                <motion.circle
                    cx="100"
                    cy="200"
                    r="35"
                    fill="#2563eb"
                    variants={itemVariants}
                    animate={{
                        rotate: 360,
                        transition: { repeat: Infinity, duration: 20, ease: "linear" },
                    }}
                />
                <motion.polygon
                    points="900,100 950,150 900,200 850,150"
                    fill="#1d4ed8"
                    variants={itemVariants}
                    animate={{
                        rotate: -360,
                        transition: { repeat: Infinity, duration: 30, ease: "linear" },
                    }}
                />
            </svg>
        </motion.div>
    )
}