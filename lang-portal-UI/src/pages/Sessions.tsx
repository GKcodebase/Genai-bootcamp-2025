
import { useState } from "react";
import { ArrowDown, ArrowUp } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { format } from "date-fns";

const Sessions = () => {
  const [sortColumn, setSortColumn] = useState("");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);

  const sessions = [
    {
      id: 1,
      groupName: "Core Verbs",
      groupId: 1,
      startTime: new Date("2024-03-15T10:00:00"),
      endTime: new Date("2024-03-15T10:30:00"),
      reviewCount: 25,
    },
    // Add more sample sessions as needed
  ];

  const handleSort = (column: string) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  };

  const SortIcon = ({ column }: { column: string }) => {
    if (sortColumn !== column) return null;
    return sortDirection === "asc" ? (
      <ArrowDown className="inline w-4 h-4 ml-1" />
    ) : (
      <ArrowUp className="inline w-4 h-4 ml-1" />
    );
  };

  return (
    <div className="animate-fadeIn">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Study Sessions</h1>
      
      <div className="bg-white rounded-lg shadow">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead onClick={() => handleSort("groupName")} className="cursor-pointer">
                Group Name <SortIcon column="groupName" />
              </TableHead>
              <TableHead onClick={() => handleSort("startTime")} className="cursor-pointer">
                Start Time <SortIcon column="startTime" />
              </TableHead>
              <TableHead onClick={() => handleSort("endTime")} className="cursor-pointer">
                End Time <SortIcon column="endTime" />
              </TableHead>
              <TableHead onClick={() => handleSort("reviewCount")} className="cursor-pointer text-right">
                # Reviews <SortIcon column="reviewCount" />
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sessions.map((session) => (
              <TableRow key={session.id}>
                <TableCell>
                  <a href={`/groups/${session.groupId}`} className="hover:text-primary">
                    {session.groupName}
                  </a>
                </TableCell>
                <TableCell>{format(session.startTime, "yyyy-MM-dd hh:mm a")}</TableCell>
                <TableCell>{format(session.endTime, "yyyy-MM-dd hh:mm a")}</TableCell>
                <TableCell className="text-right">{session.reviewCount}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <div className="flex items-center justify-between px-4 py-3 border-t">
          <button
            className="px-3 py-1 rounded bg-secondary disabled:opacity-50"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
          >
            Previous
          </button>
          <span className="text-sm text-gray-700">
            Page <span className="font-medium">{currentPage}</span> of <span className="font-medium">3</span>
          </span>
          <button
            className="px-3 py-1 rounded bg-secondary disabled:opacity-50"
            disabled={currentPage === 3}
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sessions;
