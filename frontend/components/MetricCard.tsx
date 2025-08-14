interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
  color?: 'green' | 'blue' | 'yellow' | 'red';
}

export function MetricCard({ 
  title, 
  value, 
  subtitle, 
  trend = 'neutral',
  color = 'blue' 
}: MetricCardProps) {
  const colorClasses = {
    green: 'bg-green-50 text-green-700 border-green-200',
    blue: 'bg-blue-50 text-blue-700 border-blue-200',
    yellow: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    red: 'bg-red-50 text-red-700 border-red-200',
  };
  
  const trendIcons = {
    up: '↑',
    down: '↓',
    neutral: '→'
  };
  
  return (
    <div className={`p-6 rounded-lg border-2 ${colorClasses[color]}`}>
      <h3 className="text-sm font-medium opacity-80">{title}</h3>
      <div className="mt-2 flex items-baseline">
        <p className="text-3xl font-bold">{value}</p>
        {trend !== 'neutral' && (
          <span className="ml-2 text-xl">{trendIcons[trend]}</span>
        )}
      </div>
      {subtitle && (
        <p className="mt-1 text-sm opacity-70">{subtitle}</p>
      )}
    </div>
  );
}