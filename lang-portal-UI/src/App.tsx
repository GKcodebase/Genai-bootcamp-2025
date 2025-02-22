
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/sonner";
import { Navigation } from "@/components/layout/Navigation";
import { Breadcrumbs } from "@/components/layout/Breadcrumbs";

// Page imports
import Dashboard from "@/pages/Dashboard";
import StudyActivities from "@/pages/StudyActivities";
import Words from "@/pages/Words";
import WordGroups from "@/pages/WordGroups";
import Sessions from "@/pages/Sessions";
import Settings from "@/pages/Settings";
import NotFound from "@/pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <div className="min-h-screen bg-background font-sans">
        <Navigation />
        <Breadcrumbs />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/study-activities" element={<StudyActivities />} />
            <Route path="/words" element={<Words />} />
            <Route path="/groups" element={<WordGroups />} />
            <Route path="/sessions" element={<Sessions />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
    <Toaster />
  </QueryClientProvider>
);

export default App;
