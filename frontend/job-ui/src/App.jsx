import React, { useState, useEffect } from "react";

/**
 * Base URL of the backend API
 * Change this only if backend port or host changes
 */
const API_BASE = "http://127.0.0.1:8000";

function App() {
  /* =========================
     STATE VARIABLES
     ========================= */

  // Input field for job type
  const [jobType, setJobType] = useState("email");

  // ID of the most recently created job
  const [currentJobId, setCurrentJobId] = useState(null);

  // List of all jobs created from UI
  const [jobs, setJobs] = useState([]);

  // Loading state to disable button while creating job
  const [loading, setLoading] = useState(false);

  /* =========================
     CREATE JOB
     ========================= */

  const createJob = async () => {
    try {
      setLoading(true);

      const response = await fetch(`${API_BASE}/jobs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: jobType,
          payload: {}
        })
      });

      const data = await response.json();

      // Save current job id
      setCurrentJobId(data.job_id);

      // Add job to history list
      setJobs((prevJobs) => [
        {
          id: data.job_id,
          type: jobType,
          status: "PENDING"
        },
        ...prevJobs
      ]);
    } catch (err) {
      console.error("Failed to create job", err);
    } finally {
      setLoading(false);
    }
  };

  /* =========================
     POLL JOB STATUS
     ========================= */

  useEffect(() => {
    if (!currentJobId) return;

    const interval = setInterval(async () => {
      const res = await fetch(`${API_BASE}/jobs/${currentJobId}`);
      const data = await res.json();

      // Update status in job history
      setJobs((prevJobs) =>
        prevJobs.map((job) =>
          job.id === currentJobId
            ? { ...job, status: data.status }
            : job
        )
      );

      // Stop polling once job finishes
      if (data.status === "COMPLETED" || data.status === "FAILED") {
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [currentJobId]);

  /* =========================
     STATUS COLOR HELPER
     ========================= */

  const statusColor = (status) => {
    switch (status) {
      case "PENDING":
        return "#f59e0b"; // yellow
      case "RUNNING":
        return "#3b82f6"; // blue
      case "COMPLETED":
        return "#10b981"; // green
      case "FAILED":
        return "#ef4444"; // red
      default:
        return "#6b7280";
    }
  };

  /* =========================
     UI RENDER
     ========================= */

  return (
    <div style={{
      minHeight: "100vh",
      background: "#f4f6f8",
      padding: "24px",
      fontFamily: "Arial"
    }}>
      <h2>Background Job Dashboard</h2>

      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 2fr",
        gap: "24px"
      }}>

        {/* CREATE JOB CARD */}
        <div style={{
          background: "white",
          padding: "20px",
          borderRadius: "8px"
        }}>
          <h3>Create Job</h3>

          <input
            value={jobType}
            onChange={(e) => setJobType(e.target.value)}
            placeholder="Job type"
            style={{ width: "100%", padding: "8px" }}
          />

          <button
            onClick={createJob}
            disabled={loading}
            style={{
              marginTop: "12px",
              padding: "10px",
              width: "100%",
              background: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "6px"
            }}
          >
            {loading ? "Creating..." : "Create Job"}
          </button>

          {currentJobId && (
            <>
              <p style={{ marginTop: "12px" }}>Latest Job ID:</p>
              <code>{currentJobId}</code>
            </>
          )}
        </div>

        {/* JOB HISTORY CARD */}
        <div style={{
          background: "white",
          padding: "20px",
          borderRadius: "8px"
        }}>
          <h3>Job History</h3>

          {jobs.length === 0 && <p>No jobs created yet.</p>}

          {jobs.map((job) => (
            <div
              key={job.id}
              style={{
                padding: "10px",
                borderBottom: "1px solid #e5e7eb"
              }}
            >
              <p style={{ margin: 0 }}>
                <strong>{job.type}</strong>
              </p>

              <small>{job.id}</small>

              <div style={{
                marginTop: "6px",
                display: "inline-block",
                padding: "4px 10px",
                borderRadius: "12px",
                backgroundColor: statusColor(job.status),
                color: "white",
                fontSize: "12px"
              }}>
                {job.status}
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}

export default App;
