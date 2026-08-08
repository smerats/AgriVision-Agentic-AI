import {
  Area,
  Bar,
  CartesianGrid,
  Line,
  LineChart,
  BarChart,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const chartTypes = {
  line: LineChart,
  bar: BarChart,
  area: AreaChart,
};

export default function ChartComponent({ type = 'line', data, dataKey, labelKey, title, color = '#2d8fbc' }) {
  const Chart = chartTypes[type] || LineChart;

  return (
    <div className="card chart-card">
      <div className="card-title-row">
        <h4>{title}</h4>
      </div>
      <ResponsiveContainer width="100%" height={260}>
        <Chart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e7ece7" />
          <XAxis dataKey={labelKey} tick={{ fill: '#66776b' }} />
          <YAxis tick={{ fill: '#66776b' }} />
          <Tooltip />
          {type === 'line' && <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={3} dot={{ r: 3 }} />}
          {type === 'bar' && <Bar dataKey={dataKey} fill={color} radius={[8, 8, 0, 0]} />}
          {type === 'area' && <Area type="monotone" dataKey={dataKey} stroke={color} fill={color} fillOpacity={0.15} />}
        </Chart>
      </ResponsiveContainer>
    </div>
  );
}
