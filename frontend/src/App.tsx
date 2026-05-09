import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Patient } from './types';
import { TrendBadge } from './components/TrendBadge';
import { Activity, User, PlusCircle, Search } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

function App() {
  const queryClient = useQueryClient();
  const [filter, setFilter] = useState('');

  const { data: patients, isLoading } = useQuery<Patient[]>({
    queryKey: ['patients', filter],
    queryFn: async () => {
      const url = filter ? `${API_BASE}/patients?condition=${filter}` : `${API_BASE}/patients`;
      const res = await fetch(url);
      return res.json();
    }
  });

  const mutation = useMutation({
    mutationFn: async (newOutcome: { patient_id: number; score: number }) => {
      const res = await fetch(`${API_BASE}/outcomes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newOutcome),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['patients'] });
    },
  });

  const handleAddScore = (patientId: number) => {
    const score = prompt('Enter new health score (0-100):');
    if (score !== null) {
      const numScore = parseFloat(score);
      if (!isNaN(numScore)) {
        mutation.mutate({ patient_id: patientId, score: numScore });
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <Activity className="mr-2 text-blue-600" />
              Patient Outcomes Tracker
            </h1>
            <p className="mt-2 text-sm text-gray-600">Clinical Evidence Network Monitoring</p>
          </div>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Filter by condition..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            />
          </div>
        </header>

        {isLoading ? (
          <div className="text-center py-12">Loading patients...</div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {patients?.map((patient) => (
                <li key={patient.id}>
                  <div className="px-4 py-4 flex items-center justify-between sm:px-6 hover:bg-gray-50 transition-colors">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <User className="text-blue-600 w-6 h-6" />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{patient.name}</div>
                        <div className="text-sm text-gray-500">{patient.condition} • Age {patient.age}</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="text-sm font-semibold text-gray-900">
                          Score: {patient.current_score ?? 'N/A'}
                        </div>
                        <TrendBadge trend={patient.trend} />
                      </div>
                      <button
                        onClick={() => handleAddScore(patient.id)}
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
                        title="Add Reading"
                      >
                        <PlusCircle className="w-6 h-6" />
                      </button>
                    </div>
                  </div>
                </li>
              ))}
              {patients?.length === 0 && (
                <li className="px-4 py-12 text-center text-gray-500">No patients found.</li>
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
