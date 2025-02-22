
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

const navItems = [
  { name: "Dashboard", path: "/dashboard" },
  { name: "Study Activities", path: "/study-activities" },
  { name: "Words", path: "/words" },
  { name: "Word Groups", path: "/groups" },
  { name: "Sessions", path: "/sessions" },
  { name: "Settings", path: "/settings" },
];

export function Navigation() {
  const location = useLocation();

  return (
    <nav className="border-b bg-white/80 backdrop-blur-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/dashboard" className="font-jp font-bold text-xl text-primary">
              日本語学習
            </Link>
          </div>
          <div className="flex space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "transition-colors hover:text-primary relative py-2",
                  location.pathname === item.path
                    ? "text-primary after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-primary"
                    : "text-gray-600"
                )}
              >
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}

