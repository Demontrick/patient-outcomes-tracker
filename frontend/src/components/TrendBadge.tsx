import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface TrendBadgeProps {
  trend: "Improving" | "Stable" | "Deteriorating";
}

export const TrendBadge: React.FC<TrendBadgeProps> = ({ trend }) => {
  const config = {
    Improving: {
      color: "bg-green-100 text-green-800 border-green-200",
      icon: TrendingUp,
      label: "Improving"
    },
    Stable: {
      color: "bg-blue-100 text-blue-800 border-blue-200",
      icon: Minus,
      label: "Stable"
    },
    Deteriorating: {
      color: "bg-red-100 text-red-800 border-red-200",
      icon: TrendingDown,
      label: "Deteriorating"
    }
  };

  const { color, icon: Icon, label } = config[trend];

  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border", color)}>
      <Icon className="w-3 h-3 mr-1" />
      {label}
    </span>
  );
};
