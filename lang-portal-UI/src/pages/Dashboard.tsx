
import { Card } from "@/components/ui/card";

const Dashboard = () => {
  return (
    <div className="animate-fadeIn">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome Back</h1>
        <p className="text-gray-600">Track your Japanese learning progress</p>
      </div>
      
      <section className="space-y-6">
        <h2 className="text-2xl font-semibold text-gray-900">Last Session</h2>
        <Card className="p-6">
          <p className="text-gray-600">No recent sessions found.</p>
          <button className="mt-4 inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground ring-offset-background transition-colors hover:bg-primary/90">
            Start Learning
          </button>
        </Card>
      </section>
    </div>
  );
};

export default Dashboard;

