
import { Link, useLocation } from "react-router-dom";
import { ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";

export function Breadcrumbs() {
  const location = useLocation();
  const pathSegments = location.pathname.split("/").filter(Boolean);

  return (
    <div className="bg-secondary py-2">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <Link to="/dashboard" className="hover:text-primary transition-colors">
            Home
          </Link>
          {pathSegments.map((segment, index) => (
            <div key={segment} className="flex items-center space-x-2">
              <ChevronRight className="h-4 w-4" />
              <Link
                to={`/${pathSegments.slice(0, index + 1).join("/")}`}
                className={cn(
                  "capitalize hover:text-primary transition-colors",
                  index === pathSegments.length - 1 && "text-primary font-medium"
                )}
              >
                {segment.replace(/-/g, " ")}
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

