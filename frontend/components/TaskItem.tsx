'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Circle, CheckCircle2, Edit2, Trash2, Clock, Sparkles, AlertCircle, Zap } from 'lucide-react'
import { cn } from '@/lib/cn'
import { Task } from '@/types/task'
import PriorityBadge from './PriorityBadge'
import CategoryBadge from './CategoryBadge'
import DueDateDisplay from './DueDateDisplay'

interface TaskItemProps {
  task: Task
  onToggle: (taskId: number) => Promise<void>
  onDelete: (taskId: number) => Promise<void>
  onEdit?: (task: Task) => void
}

export default function TaskItem({ task, onToggle, onDelete, onEdit }: TaskItemProps) {
  const [isHovered, setIsHovered] = useState(false)
  const [isToggling, setIsToggling] = useState(false)

  const formatDate = (isoString: string) => {
    const date = new Date(isoString)
    const now = new Date()
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)

    if (diffInSeconds < 60) return 'Just now'
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`

    return date.toLocaleDateString()
  }

  const handleToggle = async () => {
    setIsToggling(true)
    try {
      await onToggle(task.id)
    } finally {
      // Keep the animation visible for a bit
      setTimeout(() => setIsToggling(false), 400)
    }
  }

  // Priority colors mapping
  const priorityColors = {
    high: {
      border: 'border-rose-500',
      bg: 'bg-rose-500',
      glow: 'shadow-rose-500/20',
    },
    medium: {
      border: 'border-amber-500',
      bg: 'bg-amber-500',
      glow: 'shadow-amber-500/20',
    },
    low: {
      border: 'border-indigo-500',
      bg: 'bg-indigo-500',
      glow: 'shadow-indigo-500/20',
    },
  }

  // Get priority style with fallback to medium if priority is invalid
  const priorityStyle = priorityColors[task.priority] || priorityColors.medium

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
      whileHover={{ y: -2 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className={cn(
        'group relative bg-white rounded-2xl border-2 transition-all duration-300',
        'hover:shadow-xl',
        task.completed
          ? 'border-slate-200 bg-slate-50/50 opacity-75'
          : cn(
              'border-slate-200',
              isHovered && 'border-indigo-300 shadow-lg shadow-indigo-100/50'
            )
      )}
    >
      {/* Priority Indicator Bar - More prominent */}
      <div
        className={cn(
          'absolute left-0 top-0 bottom-0 w-1.5 rounded-l-2xl transition-all duration-300',
          priorityStyle.bg,
          isHovered && !task.completed && 'w-2'
        )}
      />

      {/* Glow effect on hover for incomplete tasks */}
      {isHovered && !task.completed && (
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-indigo-500/5 to-purple-500/5 pointer-events-none" />
      )}

      <div className="flex items-start gap-4 p-5">
        {/* Spacer for left icon (we show completion on the right action area) */}
        <div className="flex-shrink-0 mt-1 w-6" aria-hidden="true" />

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          {/* Title with High Priority Icon */}
          <div className="flex items-center gap-2 mb-2.5">
            {task.priority === 'high' && (
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="flex-shrink-0"
              >
                <Zap className="w-5 h-5 text-rose-500 fill-rose-500" />
              </motion.div>
            )}
            <motion.h3
              layout
              className={cn(
                'text-base font-semibold leading-snug transition-colors duration-200',
                task.completed
                  ? 'line-through text-slate-400'
                  : 'text-slate-900'
              )}
            >
              {task.title}
            </motion.h3>
          </div>

          {/* Badges Row */}
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <PriorityBadge priority={task.priority} size="sm" />
            {task.category && <CategoryBadge category={task.category} size="sm" />}
            {task.due_date && (
              <DueDateDisplay dueDate={task.due_date} completed={task.completed} size="sm" />
            )}
          </div>

          {/* Description */}
          {task.description && (
            <p
              className={cn(
                'text-sm mb-3 break-words leading-relaxed transition-colors duration-200',
                task.completed ? 'text-slate-400' : 'text-slate-600'
              )}
            >
              {task.description}
            </p>
          )}

          {/* Footer - Created At */}
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <Clock className="w-3.5 h-3.5" />
            <span>Created {formatDate(task.created_at)}</span>
          </div>
        </div>

        {/* Action Buttons - Always Visible with Priority and Status */}
        <div className="flex-shrink-0 flex items-center gap-2">
          {/* Priority Badge - Always Show */}
          <div className="flex items-center gap-1 px-2.5 py-1.5 bg-slate-900/5 rounded-lg">
            <PriorityBadge priority={task.priority} size="sm" />
          </div>

          {/* Completion Status Indicator */}
          <div className="flex items-center">
            {task.completed ? (
              <motion.div
                initial={{ scale: 0.8, rotate: -90 }}
                animate={{ scale: 1, rotate: 0 }}
                className="text-emerald-500 px-2"
              >
                <CheckCircle2 className="w-5 h-5" />
              </motion.div>
            ) : (
              <motion.button
                onClick={handleToggle}
                disabled={isToggling}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="text-slate-400 hover:text-indigo-500 px-2 transition-colors"
                aria-label="Toggle task completion"
              >
                <Circle className="w-5 h-5" />
              </motion.button>
            )}
          </div>

          {/* Edit Button */}
          {onEdit && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onEdit(task)}
              className="p-2 rounded-lg text-slate-500 hover:text-indigo-500 hover:bg-indigo-50/50 transition-colors"
              aria-label="Edit task"
            >
              <Edit2 className="w-5 h-5" />
            </motion.button>
          )}

          {/* Delete Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onDelete(task.id)}
            className="p-2 rounded-lg text-slate-500 hover:text-rose-500 hover:bg-rose-50/50 transition-colors"
            aria-label="Delete task"
          >
            <Trash2 className="w-5 h-5" />
          </motion.button>
        </div>
      </div>

      {/* Completion celebration effect */}
      {task.completed && isToggling && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0 }}
          className="absolute top-2 right-2"
        >
          <Sparkles className="w-5 h-5 text-emerald-500" />
        </motion.div>
      )}
    </motion.div>
  )
}
