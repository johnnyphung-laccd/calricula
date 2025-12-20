'use client';

// ===========================================
// Workflow History Panel Component
// ===========================================
// Timeline view showing complete workflow history for a course or program
// Shows status transitions, who made changes, timestamps, and comments

import { useState, useEffect } from 'react';
import {
  ClockIcon,
  ArrowRightIcon,
  ChatBubbleLeftIcon,
  UserCircleIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';
import { useAuth } from '@/contexts/AuthContext';
import { api, WorkflowHistoryItem } from '@/lib/api';

// ===========================================
// Types
// ===========================================

interface WorkflowHistoryPanelProps {
  entityType: 'Course' | 'Program';
  entityId: string;
  className?: string;
}

// ===========================================
// Status Configuration
// ===========================================

const STATUS_LABELS: Record<string, string> = {
  Draft: 'Draft',
  DeptReview: 'Department Review',
  CurriculumCommittee: 'Curriculum Committee',
  ArticulationReview: 'Articulation Review',
  Approved: 'Approved',
  Review: 'Under Review',
};

const STATUS_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  Draft: { bg: 'bg-gray-100', text: 'text-gray-700', border: 'border-gray-300' },
  DeptReview: { bg: 'bg-blue-100', text: 'text-blue-700', border: 'border-blue-300' },
  CurriculumCommittee: { bg: 'bg-amber-100', text: 'text-amber-700', border: 'border-amber-300' },
  ArticulationReview: { bg: 'bg-purple-100', text: 'text-purple-700', border: 'border-purple-300' },
  Approved: { bg: 'bg-green-100', text: 'text-green-700', border: 'border-green-300' },
  Review: { bg: 'bg-blue-100', text: 'text-blue-700', border: 'border-blue-300' },
};

const ROLE_BADGES: Record<string, { bg: string; text: string }> = {
  Faculty: { bg: 'bg-slate-100', text: 'text-slate-600' },
  CurriculumChair: { bg: 'bg-blue-100', text: 'text-blue-600' },
  ArticulationOfficer: { bg: 'bg-purple-100', text: 'text-purple-600' },
  Admin: { bg: 'bg-red-100', text: 'text-red-600' },
};

// ===========================================
// Helper Functions
// ===========================================

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}

function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return formatDate(dateString);
}

function getStatusColor(status: string) {
  return STATUS_COLORS[status] || STATUS_COLORS.Draft;
}

function getRoleBadge(role: string) {
  return ROLE_BADGES[role] || ROLE_BADGES.Faculty;
}

function getStatusLabel(status: string): string {
  return STATUS_LABELS[status] || status;
}

// ===========================================
// Status Badge Component
// ===========================================

function StatusBadge({ status }: { status: string }) {
  const colors = getStatusColor(status);
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors.bg} ${colors.text} border ${colors.border}`}
    >
      {getStatusLabel(status)}
    </span>
  );
}

// ===========================================
// Role Badge Component
// ===========================================

function RoleBadge({ role }: { role: string }) {
  const colors = getRoleBadge(role);
  const displayRole = role.replace(/([A-Z])/g, ' $1').trim();
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${colors.bg} ${colors.text}`}
    >
      {displayRole}
    </span>
  );
}

// ===========================================
// Timeline Item Component
// ===========================================

function TimelineItem({
  item,
  isFirst,
  isLast,
}: {
  item: WorkflowHistoryItem;
  isFirst: boolean;
  isLast: boolean;
}) {
  const isApproval = item.to_status === 'Approved';
  const isReturn = item.to_status === 'Draft' && item.from_status !== 'Draft';

  return (
    <div className="relative pb-8">
      {/* Connecting line */}
      {!isLast && (
        <span
          className="absolute left-4 top-8 -ml-px h-full w-0.5 bg-gray-200"
          aria-hidden="true"
        />
      )}

      <div className="relative flex items-start space-x-3">
        {/* Icon */}
        <div className="relative">
          <div
            className={`flex h-8 w-8 items-center justify-center rounded-full ring-4 ring-white ${
              isApproval
                ? 'bg-green-500'
                : isReturn
                ? 'bg-amber-500'
                : 'bg-luminous-500'
            }`}
          >
            {isApproval ? (
              <CheckCircleIcon className="h-5 w-5 text-white" />
            ) : isReturn ? (
              <ArrowPathIcon className="h-5 w-5 text-white" />
            ) : (
              <ArrowRightIcon className="h-4 w-4 text-white" />
            )}
          </div>
        </div>

        {/* Content */}
        <div className="min-w-0 flex-1">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <StatusBadge status={item.from_status} />
              <ArrowRightIcon className="h-4 w-4 text-gray-400" />
              <StatusBadge status={item.to_status} />
            </div>
            <div className="text-xs text-gray-500" title={formatDate(item.created_at)}>
              {formatRelativeTime(item.created_at)}
            </div>
          </div>

          {/* User info */}
          <div className="mt-2 flex items-center space-x-2 text-sm text-gray-600">
            <UserCircleIcon className="h-4 w-4 text-gray-400" />
            <span className="font-medium">
              {item.user?.full_name || 'Unknown User'}
            </span>
            {item.user?.role && <RoleBadge role={item.user.role} />}
          </div>

          {/* Comment */}
          {item.comment && (
            <div className="mt-2 rounded-lg bg-gray-50 p-3 text-sm text-gray-700">
              <div className="flex items-start space-x-2">
                <ChatBubbleLeftIcon className="h-4 w-4 text-gray-400 mt-0.5 flex-shrink-0" />
                <p className="whitespace-pre-wrap">{item.comment}</p>
              </div>
            </div>
          )}

          {/* Timestamp */}
          <div className="mt-1 flex items-center text-xs text-gray-400">
            <ClockIcon className="h-3 w-3 mr-1" />
            {formatDate(item.created_at)}
          </div>
        </div>
      </div>
    </div>
  );
}

// ===========================================
// Empty State Component
// ===========================================

function EmptyState({ entityType }: { entityType: string }) {
  return (
    <div className="text-center py-12">
      <ClockIcon className="mx-auto h-12 w-12 text-gray-300" />
      <h3 className="mt-2 text-sm font-semibold text-gray-900">No history yet</h3>
      <p className="mt-1 text-sm text-gray-500">
        Workflow history will appear here as the {entityType.toLowerCase()} moves through the approval process.
      </p>
    </div>
  );
}

// ===========================================
// Loading State Component
// ===========================================

function LoadingState() {
  return (
    <div className="space-y-6 animate-pulse">
      {[1, 2, 3].map((i) => (
        <div key={i} className="flex items-start space-x-3">
          <div className="h-8 w-8 rounded-full bg-gray-200" />
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-gray-200 rounded w-3/4" />
            <div className="h-3 bg-gray-200 rounded w-1/2" />
          </div>
        </div>
      ))}
    </div>
  );
}

// ===========================================
// Main Component
// ===========================================

export function WorkflowHistoryPanel({
  entityType,
  entityId,
  className = '',
}: WorkflowHistoryPanelProps) {
  const { getToken } = useAuth();
  const [history, setHistory] = useState<WorkflowHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchHistory() {
      try {
        setLoading(true);
        setError(null);

        const token = await getToken();
        if (token) {
          api.setToken(token);
        }

        const data = await api.getWorkflowHistory(entityType, entityId);
        setHistory(data);
      } catch (err) {
        console.error('Failed to fetch workflow history:', err);
        setError('Failed to load workflow history. Please try again.');
      } finally {
        setLoading(false);
      }
    }

    fetchHistory();
  }, [entityType, entityId, getToken]);

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <ClockIcon className="h-5 w-5 text-gray-500" />
          <h3 className="text-lg font-semibold text-gray-900">Workflow History</h3>
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Timeline of status changes and approval actions
        </p>
      </div>

      {/* Content */}
      <div className="p-4">
        {loading ? (
          <LoadingState />
        ) : error ? (
          <div className="text-center py-8">
            <XCircleIcon className="mx-auto h-12 w-12 text-red-400" />
            <p className="mt-2 text-sm text-red-600">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 text-sm font-medium text-luminous-600 hover:text-luminous-500"
            >
              Try again
            </button>
          </div>
        ) : history.length === 0 ? (
          <EmptyState entityType={entityType} />
        ) : (
          <div className="flow-root">
            <ul className="-mb-8">
              {history.map((item, idx) => (
                <li key={item.id}>
                  <TimelineItem
                    item={item}
                    isFirst={idx === 0}
                    isLast={idx === history.length - 1}
                  />
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Footer with count */}
      {!loading && history.length > 0 && (
        <div className="px-4 py-3 border-t border-gray-200 bg-gray-50 rounded-b-lg">
          <p className="text-xs text-gray-500">
            {history.length} status {history.length === 1 ? 'change' : 'changes'} recorded
          </p>
        </div>
      )}
    </div>
  );
}

export default WorkflowHistoryPanel;
