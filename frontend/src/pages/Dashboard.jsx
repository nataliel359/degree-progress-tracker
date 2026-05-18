import { useEffect, useState } from "react";
import { getProgress } from "../api/client";
import "../styles/Dashboard.css";

export default function Dashboard() {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetchProgress();
    }, []);

    const fetchProgress = async () => {
        try {
            const response = await getProgress();
            console.log(response);
            setData(response);
        } catch (error) {
            console.error(error);
        }
    };

    if (!data) return <div>Loading...</div>;

    return (
        <div className="dashboard">
            <h1>{data.student}</h1>
            <ProgramSection title="Computer Science Major" data={data.major} />
            <ProgramSection title="Business Minor" data={data.minor} />
        </div>
    );
}

function ProgramSection({ title, data }) {
    const { summary, requirements } = data;

    return (
        <div className="program-card">
            {/* HEADER */}
            <div className="program-header">
                <div>
                    <h2>{title}</h2>
                    <p>{summary.total_completed} / {summary.total_required} credits</p>
                </div>
                <div className="percent-badge">
                    {summary.progress_percent}%
                </div>
            </div>

            {/* OVERALL BAR */}
            <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${summary.progress_percent}%` }} />
            </div>

            {/* REQUIREMENTS */}
            <div className="requirements">
                {Object.entries(requirements).map(
                    ([key, section]) => {
                        const percent = section.required === 0 ? 100 : Math.round((section.completed / section.required) * 100);
                        return (
                            <div key={key} className="requirement-card">
                                <div className="requirement-header">
                                    <div>
                                        <h3>{formatTitle(key)}</h3>
                                        <p>{section.completed} / {section.required} credits</p>
                                    </div>
                                    <div className="small-badge">{percent}%</div>
                                </div>
                               
                               {/* SECTION BAR */}
                                <div className="progress-bar">
                                    <div className="progress-fill" style={{ width: `${percent}%` }} />
                                </div>
                                
                                {/* COURSES */}
                                <div className="course-grid">
                                    {/* COMPLETED */}
                                    <div>
                                        <h4 className="green">Completed</h4>
                                        {section.completed_courses.map(
                                            (course, index) => (
                                                <div key={index} className="course-card completed">
                                                    <div>
                                                        <strong>{course.code}</strong><p>{course.name}</p>
                                                    </div>
                                                    <span>{course.credits} credits</span>
                                                </div>
                                            )
                                        )}
                                    </div>

                                    {/* MISSING */}
                                    <div>
                                        <h4 className="red">Missing</h4>
                                        {section.missing_courses.map(
                                            (course, index) => (
                                                <div key={index} className="course-card missing">
                                                    <div>
                                                        <strong>{course.code}</strong><p>{course.name}</p>
                                                    </div>
                                                    <span>{course.credits} credits</span>
                                                </div>
                                            )
                                        )}
                                    </div>
                                </div>
                            </div>
                        )
                    }
                )}
            </div>
        </div>
    );
}

function formatTitle(key) {
    return key.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}