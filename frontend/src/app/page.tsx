'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import Image from 'next/image'
export default function Component() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const router = useRouter()

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }

    window.addEventListener('mousemove', handleMouseMove)

    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
    }
  }, [])

  return (
    <div className="relative h-screen w-full overflow-hidden bg-blue400">
      <motion.div
        className="absolute inset-0 bg-blue-300"
        animate={{
          clipPath: `circle(${mousePosition.x * 0.1 + mousePosition.y * 0.1 + 200}px at ${mousePosition.x}px ${mousePosition.y}px)`,
        }}
        transition={{ type: 'spring', stiffness: 20, damping: 30 }}
      />
      <div className="relative z-10 flex h-full flex-col items-center justify-center text-blue-500">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
        >
          <Image
            src="/images/databaelogo.png" // Route of the image file
            height={196} // Desired size with correct aspect ratio
            width={196} // Desired size with correct aspect ratio
            alt="LOGO"
          />
        </motion.div>
        <motion.h1
          className="mb-4 text-8xl font-bold"
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
        >
          databae.
        </motion.h1>
        <motion.p
          className="mb-8 text-xl text-blue-500"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}
        >
          Simplify Database!
        </motion.p>
        <motion.button
          className="rounded-full bg-blue-600 px-8 py-3 text-lg font-semibold text-white shadow-lg transition-colors hover:bg-blue-50"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => router.push('/connection')}
        >
          Get started
        </motion.button>
      </div>
    </div>
  )
}