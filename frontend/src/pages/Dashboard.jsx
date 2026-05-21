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

    const overallRequired = data.major.summary.total_required + data.minor.summary.total_required;
    const overallCompleted = data.major.summary.total_completed + data.minor.summary.total_completed;
    const overallPercent = Math.round((overallCompleted / overallRequired) * 100);

    return (
        <div className="dashboard">
            {/* HERO */}
            <div className="student-hero">
                <div className="student-info">
                    <div className="avatar">
                        {data.student.charAt(0)}
                    </div>
                    <div>
                        <h1>{data.student}</h1>
                        <p className="student-meta">Honours Bachelor of Science - Computer Science Major / Business Minor</p>
                        <p className="student-meta">Lassonde School of Engineering</p>
                        <p className="student-meta">Student ID: 202319845</p>
                    </div>
                </div>
                <div className="overall-progress-card">
                    <div className="overall-percent">
                        <p>Overall Progress</p>
                        <p>{overallPercent}%</p>
                        <a href="https://registrar.yorku.ca/graduation/apply" className="convocation-link">Apply for Convocation</a>
                    </div>
                </div>
                
            </div>

            {/* LEFT CONTENT */}
            <div className="main-content">
                {/* PROGRAM SECTIONS */}
                <ProgramSection title="Computer Science Major" data={data.major} />
                <ProgramSection title="Business Minor" data={data.minor} />
            </div>

            {/* RIGHT SIDEBAR */}
            <div className="sidebar">
                <div className="sidebar-card">
                    <h3>Useful Links</h3>
                    <div className="link-list">
                        <a href="https://students.yorku.ca/myonlineservices" className="small-badge">Online Services</a><br />
                        <a href="https://students.yorku.ca/york-gpa-calculator" className="small-badge">GPA Calculator</a><br />
                        {/* <a href="https://lassonde.yorku.ca/student-life/connect-with-an-academic-advisor" className="small-badge">Connect with an Advisor</a>
                        <a href="https://lassonde.yorku.ca/co-op/" className="small-badge">Co-op Info</a> */}
                        <a href="https://myacademicrecord.students.yorku.ca/program-change" className="small-badge">Degree Change Request</a><br />
                        <a href="https://students.yorku.ca/sfs/scholarships-awards-bursaries" className="small-badge">Awards Search</a>
                    </div>
                </div>
            </div>
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