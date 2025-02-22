
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

const StudyActivities = () => {
  const activities = [
    {
      id: 1,
      title: "Adventure MUD",
      thumbnail: "/placeholder.svg",
      description: "Interactive text-based adventure game for learning Japanese",
    },
    {
      id: 2,
      title: "Typing Tutor",
      thumbnail: "/placeholder.svg",
      description: "Practice typing Japanese characters",
    },
  ];

  return (
    <div className="animate-fadeIn">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Study Activities</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {activities.map((activity) => (
          <Card key={activity.id} className="overflow-hidden">
            <CardHeader className="p-0">
              <img
                src={activity.thumbnail}
                alt={activity.title}
                className="w-full h-48 object-cover"
              />
            </CardHeader>
            <CardContent className="p-6">
              <CardTitle className="mb-2">{activity.title}</CardTitle>
              <p className="text-gray-600">{activity.description}</p>
            </CardContent>
            <CardFooter className="p-6 pt-0 flex gap-4">
              <button
                onClick={() => window.open(`http://localhost:8081?group_id=${activity.id}`, '_blank')}
                className="flex-1 bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md"
              >
                Launch
              </button>
              <button
                onClick={() => window.location.href = `/study-activities/${activity.id}`}
                className="flex-1 bg-secondary text-secondary-foreground hover:bg-secondary/80 px-4 py-2 rounded-md"
              >
                View
              </button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default StudyActivities;
