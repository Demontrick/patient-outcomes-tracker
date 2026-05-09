import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TrendBadge } from './components/TrendBadge';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

describe('TrendBadge', () => {
  it('renders Improving trend correctly', () => {
    render(<TrendBadge trend="Improving" />);
    expect(screen.getByText('Improving')).toBeInTheDocument();
  });

  it('renders Deteriorating trend correctly', () => {
    render(<TrendBadge trend="Deteriorating" />);
    expect(screen.getByText('Deteriorating')).toBeInTheDocument();
  });

  it('renders Stable trend correctly', () => {
    render(<TrendBadge trend="Stable" />);
    expect(screen.getByText('Stable')).toBeInTheDocument();
  });
});

describe('App', () => {
  it('renders the header title', () => {
    render(<App />, { wrapper });
    expect(screen.getByText('Patient Outcomes Tracker')).toBeInTheDocument();
  });

  it('shows loading state initially', () => {
    render(<App />, { wrapper });
    expect(screen.getByText('Loading patients...')).toBeInTheDocument();
  });
});
