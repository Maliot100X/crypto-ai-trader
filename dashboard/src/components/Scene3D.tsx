'use client'

import { useRef, useMemo, useCallback } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, Float, Text, Sphere, Line } from '@react-three/drei'
import * as THREE from 'three'

// Particle field background
function ParticleField({ count = 2000 }) {
  const mesh = useRef<THREE.Points>(null!)
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3)
    for (let i = 0; i < count * 3; i++) {
      pos[i] = (Math.random() - 0.5) * 100
    }
    return pos
  }, [count])

  const colors = useMemo(() => {
    const cols = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const t = Math.random()
      // Gradient between purple, green, and blue
      cols[i * 3] = 0.6 * (1 - t) + 0.0 * t     // R
      cols[i * 3 + 1] = 0.27 * (1 - t) + 0.95 * t // G
      cols[i * 3 + 2] = 1.0 * (1 - t) + 0.6 * t   // B
    }
    return cols
  }, [count])

  useFrame((state) => {
    if (mesh.current) {
      mesh.current.rotation.y = state.clock.elapsedTime * 0.02
      mesh.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.01) * 0.1
    }
  })

  return (
    <points ref={mesh}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
        <bufferAttribute attach="attributes-color" count={count} array={colors} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial size={0.15} vertexColors transparent opacity={0.6} sizeAttenuation />
    </points>
  )
}

// Agent node in 3D space
function AgentNode({ position, label, color = '#14F195', active = true }: {
  position: [number, number, number]
  label: string
  color?: string
  active?: boolean
}) {
  const meshRef = useRef<THREE.Mesh>(null!)
  const glowRef = useRef<THREE.Mesh>(null!)

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime * 2 + position[0]) * 0.1)
    }
    if (glowRef.current) {
      const mat = glowRef.current.material as THREE.MeshBasicMaterial
      mat.opacity = 0.15 + Math.sin(state.clock.elapsedTime * 3 + position[1]) * 0.1
    }
  })

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
      <group position={position}>
        {/* Core sphere */}
        <mesh ref={meshRef}>
          <sphereGeometry args={[0.4, 32, 32]} />
          <meshStandardMaterial color={active ? color : '#555'} emissive={active ? color : '#333'} emissiveIntensity={0.5} />
        </mesh>
        {/* Glow sphere */}
        <mesh ref={glowRef} scale={2}>
          <sphereGeometry args={[0.4, 16, 16]} />
          <meshBasicMaterial color={color} transparent opacity={0.15} />
        </mesh>
        {/* Label */}
        <Text position={[0, -0.8, 0]} fontSize={0.25} color="#ffffff" anchorX="center" anchorY="top">
          {label}
        </Text>
      </group>
    </Float>
  )
}

// Connection line between agents
function AgentConnection({ start, end, color = '#9945FF' }: {
  start: [number, number, number]
  end: [number, number, number]
  color?: string
}) {
  const ref = useRef<any>(null!)

  useFrame((state) => {
    if (ref.current) {
      const mat = ref.current.material
      if (mat) {
        mat.opacity = 0.2 + Math.sin(state.clock.elapsedTime * 2) * 0.15
      }
    }
  })

  return (
    <Line
      ref={ref}
      points={[start, end]}
      color={color}
      lineWidth={1}
      transparent
      opacity={0.3}
    />
  )
}

// Orbiting ring
function OrbitRing({ radius = 8, color = '#9945FF' }) {
  const ref = useRef<THREE.Mesh>(null!)
  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.z = state.clock.elapsedTime * 0.15
      ref.current.rotation.x = Math.PI / 2 + Math.sin(state.clock.elapsedTime * 0.1) * 0.2
    }
  })
  return (
    <mesh ref={ref}>
      <torusGeometry args={[radius, 0.02, 16, 100]} />
      <meshBasicMaterial color={color} transparent opacity={0.3} />
    </mesh>
  )
}

// Data stream visualization
function DataStream() {
  const ref = useRef<THREE.Points>(null!)
  const count = 200

  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2 * 3
      const radius = 5 + Math.sin(i * 0.1) * 2
      pos[i * 3] = Math.cos(angle) * radius
      pos[i * 3 + 1] = (i / count - 0.5) * 10
      pos[i * 3 + 2] = Math.sin(angle) * radius
    }
    return pos
  }, [])

  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.y = state.clock.elapsedTime * 0.3
    }
  })

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial size={0.08} color="#00D1FF" transparent opacity={0.5} />
    </points>
  )
}

// Central core
function CoreSphere() {
  const ref = useRef<THREE.Mesh>(null!)
  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.y = state.clock.elapsedTime * 0.5
      ref.current.rotation.z = state.clock.elapsedTime * 0.3
    }
  })
  return (
    <mesh ref={ref}>
      <icosahedronGeometry args={[1.2, 2]} />
      <meshStandardMaterial color="#9945FF" wireframe emissive="#9945FF" emissiveIntensity={0.3} />
    </mesh>
  )
}

// Agent network with connections
function AgentNetwork({ agents }: { agents: Array<{ id: string; position: [number, number, number]; active: boolean }> }) {
  const colors = ['#14F195', '#9945FF', '#00D1FF', '#FF6B6B', '#FFD93D']
  return (
    <group>
      {agents.map((agent, i) => (
        <AgentNode
          key={agent.id}
          position={agent.position}
          label={agent.id}
          color={colors[i % colors.length]}
          active={agent.active}
        />
      ))}
      {agents.map((a, i) =>
        agents.slice(i + 1).map((b, j) => (
          <AgentConnection
            key={`${a.id}-${b.id}`}
            start={a.position}
            end={b.position}
            color={colors[(i + j) % colors.length]}
          />
        ))
      )}
    </group>
  )
}

// Main 3D Scene
export default function Scene3D({ agents, fullScreen = false }: {
  agents?: Array<{ id: string; status: string }>
  fullScreen?: boolean
}) {
  const defaultAgents = agents?.map((a, i) => ({
    id: a.id,
    position: [
      Math.cos((i / (agents.length || 1)) * Math.PI * 2) * 6,
      Math.sin(i * 1.5) * 2,
      Math.sin((i / (agents.length || 1)) * Math.PI * 2) * 6,
    ] as [number, number, number],
    active: a.status === 'running',
  })) || [
    { id: 'Agent Alpha', position: [5, 1, 0] as [number, number, number], active: true },
    { id: 'Agent Beta', position: [-3, 2, 4] as [number, number, number], active: true },
    { id: 'Agent Gamma', position: [-2, -1, -5] as [number, number, number], active: true },
    { id: 'Agent Delta', position: [4, -2, -3] as [number, number, number], active: false },
    { id: 'Agent Omega', position: [-5, 0, 2] as [number, number, number], active: true },
  ]

  return (
    <div className={fullScreen ? 'fixed inset-0 -z-10' : 'w-full h-[500px] rounded-2xl overflow-hidden'}>
      <Canvas
        camera={{ position: [0, 5, 15], fov: 60 }}
        gl={{ antialias: true, alpha: true }}
        style={{ background: 'transparent' }}
      >
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#9945FF" />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#14F195" />
        <pointLight position={[0, 10, 0]} intensity={0.3} color="#00D1FF" />

        <ParticleField count={3000} />
        <CoreSphere />
        <AgentNetwork agents={defaultAgents} />
        <OrbitRing radius={10} color="#9945FF" />
        <OrbitRing radius={7} color="#14F195" />
        <DataStream />

        <OrbitControls
          enableZoom={true}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.5}
          maxPolarAngle={Math.PI / 1.5}
          minPolarAngle={Math.PI / 4}
        />
      </Canvas>
    </div>
  )
}
