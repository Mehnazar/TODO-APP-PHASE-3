import { TaskPriority } from '@/types/task'
import { AlertCircle, ArrowUp, Minus } from 'lucide-react'

interface PriorityBadgeProps {
  priority: TaskPriority
  size?: 'sm' | 'md' | 'lg'
}

const priorityConfig = {
  high: {
    label: 'High',
    icon: ArrowUp,
    bgColor: 'bg-rose-500/20',
    textColor: 'text-rose-400',
    borderColor: 'border-rose-500/30',
    iconColor: 'text-rose-400',
  },
  medium: {
    label: 'Medium',
    icon: AlertCircle,
    bgColor: 'bg-yellow-500/20',
    textColor: 'text-yellow-400',
    borderColor: 'border-yellow-500/30',
    iconColor: 'text-yellow-400',
  },
  low: {
    label: 'Low',
    icon: Minus,
    bgColor: 'bg-cyan-500/20',
    textColor: 'text-cyan-400',
    borderColor: 'border-cyan-500/30',
    iconColor: 'text-cyan-400',
  },
}

export default function PriorityBadge({ priority, size = 'md' }: PriorityBadgeProps) {
  const config = priorityConfig[priority] || priorityConfig.medium
  const Icon = config.icon

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base',
  }

  const iconSizeClasses = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  }

  return (
    <span
      className={`
        inline-flex items-center gap-1.5 rounded-full font-medium border
        ${config.bgColor} ${config.textColor} ${config.borderColor}
        ${sizeClasses[size]}
      `}
    >
      <Icon className={`${iconSizeClasses[size]} ${config.iconColor}`} />
      <span>{config.label}</span>
    </span>
  )
}
