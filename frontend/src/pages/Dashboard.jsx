import { useEffect, useState } from "react";
import { getProgress } from "../api/client";
import "../styles/Dashboard.css";

import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Dashboard() {
    const [selectedCourse, setSelectedCourse] = useState(null);
    const openCourseModal = (course) => {
        setSelectedCourse(course);
    };
    const closeCourseModal = () => {
        setSelectedCourse(null);
    };

    const [data, setData] = useState(null);
    const navigate = useNavigate();
    const { logout } = useAuth();

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

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    if (!data) return <div className="loading">Loading...</div>;

    const overallRequired = data.major.summary.total_required + data.minor.summary.total_required;
    const overallCompleted = data.major.summary.total_completed + data.minor.summary.total_completed;
    const overallPercent = Math.round((overallCompleted / overallRequired) * 100);

    return (
        <div className="dashboard">
            {/* HERO */}
            <StudentHero
                student={data.student}
                overallPercent={overallPercent}
                overallCompleted={overallCompleted}
                overallRequired={overallRequired}
                onLogout={handleLogout}
            />

            {/* LEFT CONTENT */}
            <div className="main-content">
                {/* PROGRAM SECTIONS */}
                <ProgramSection title="Computer Science Major" subtitle="Core requirements for BSC Honours degree" data={data.major} onCompletedCourseClick={openCourseModal} />
                <ProgramSection title="Business Minor" subtitle="Complementary business credential" data={data.minor} onCompletedCourseClick={openCourseModal} />
            </div>

            {/* RIGHT SIDEBAR */}
            <aside className="sidebar">
                {/* <UsefulLinks /> */}
                <div className="sidebar-card">
                    <h3>Useful Links</h3>
                    <div className="link-list">
                        <a href="https://students.yorku.ca/myonlineservices" className="small-badge">Online Services</a>
                        <a href="https://students.yorku.ca/york-gpa-calculator" className="small-badge">GPA Calculator</a>
                        <a href="https://lassonde.yorku.ca/student-life/connect-with-an-academic-advisor" className="small-badge">Connect with an Advisor</a>
                        <a href="https://lassonde.yorku.ca/co-op/" className="small-badge">Co-op Info</a>
                        <a href="https://myacademicrecord.students.yorku.ca/program-change" className="small-badge">Degree Change Request</a>
                        <a href="https://students.yorku.ca/sfs/scholarships-awards-bursaries" className="small-badge">Awards Search</a>
                    </div>
                </div>
            </aside>

            {selectedCourse && (
                <CourseModal course={selectedCourse} onClose={closeCourseModal} />
            )}
        </div>
    );
}

function StudentHero({
    student,
    overallPercent,
    overallCompleted,
    overallRequired,
    onLogout
}) {
    return (
        <section className="student-hero">
            <div className="student-info">
                {/* <div className="avatar">{student.charAt(0)}</div> */}
                <div>
                    <p className="eyebrow">Degree Progress Tracker</p>
                    <h1 style={{ color: 'white' }}>{student}</h1>
                    <p className="student-meta">Honours Bachelor of Science - Computer Science Major / Business Minor</p>
                    <p className="student-meta">Lassonde School of Engineering</p>
                    <p className="student-meta">Student ID: 202319845</p>
                </div>
            </div>
            <div className="overall-progress-card">
                <div className="overall-label"><p>Overall Progress</p></div>
                <div className="overall-row">
                    <strong>{overallPercent}%</strong>
                    <span>{overallCompleted} / {overallRequired} credits</span>
                </div>

                <div className="progress-bar hero-progress">
                    <div className={`progress-fill ${getProgressColorClass(overallPercent)}`} style={{ width: `${overallPercent}%` }} />
                </div>
                <a href="https://registrar.yorku.ca/graduation/apply" className="convocation-link">Apply for Convocation</a>
                <br />
                <button className="signout-button" onClick={onLogout}>Sign out</button>
            </div>
        </section>
    );
}

function ProgramSection({ title, data, onCompletedCourseClick }) {
    const [viewMode, setViewMode] = useState("all");
    const { summary, requirements } = data;

    return (
        <section className="program-card">
            {/* HEADER */}
            <div className="program-header">
                <div>
                    <h2>{title}</h2>
                    <p>{summary.total_completed} / {summary.total_required} credits</p>
                </div>
                <div className="percent-badge">{summary.progress_percent}%</div>
            </div>

            {/* OVERALL BAR */}
            <div className="progress-bar">
                <div className={`progress-fill ${getProgressColorClass(summary.progress_percent)}`} style={{ width: `${summary.progress_percent}%` }} />
            </div>

            <div className="view-toggle">
                <button className={viewMode === "all" ? "active" : ""} onClick={() => setViewMode("all")}>All</button>
                <button className={viewMode === "completed" ? "active" : ""} onClick={() => setViewMode("completed")}>Completed</button>
            </div>

            {/* REQUIREMENTS */}
            <div className="requirements">
                {Object.entries(requirements).map(([key, section]) => (
                    <RequirementSection
                        key={key}
                        title={formatTitle(key)}
                        section={section}
                        viewMode={viewMode}
                        onCompletedCourseClick={onCompletedCourseClick}
                    />
                ))}
            </div>
        </section>
    );
}

function RequirementSection({ title, section, viewMode, onCompletedCourseClick }) {
    const percent = section.required === 0 ? 100 : Math.round((section.completed / section.required) * 100);
    const showMissing = viewMode === "all";

    return (
        <div className="requirement-card">
            <div className="requirement-header">
                <div>
                    <h3>{title}</h3>
                    <p>{section.completed} / {section.required} credits</p>
                </div>
                <div className="small-badge">{percent}%</div>
            </div>

            <div className="progress-bar">
                <div className={`progress-fill ${getProgressColorClass(percent)}`} style={{ width: `${percent}%` }} />
            </div>

            <div className={showMissing ? "course-grid" : "course-grid completed-only"}>
                <div>
                    <h4 className="green">Completed ({section.completed_courses.length})</h4>
                    {section.completed_courses.map((course, index) => (
                        <CourseCard
                            key={`${course.code}-${index}`}
                            course={course}
                            status="completed"
                            onCourseClick={() => onCompletedCourseClick && onCompletedCourseClick(course)}
                        />
                    ))}
                </div>
                    
                {showMissing && (
                    <div>
                        <h4 className="red">Missing ({section.missing_courses.length})</h4>
                        {section.missing_courses.map((course, index) => (
                            <CourseCard
                                key={`${course.code}-${index}`}
                                course={course}
                                status="missing"
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}

function CourseCard({ course, status, onCourseClick }) {
    const isCompleted = status === "completed";

    return (
        <button type="button" className={`course-card ${status}`} onClick={isCompleted ? onCourseClick : undefined} disabled={!isCompleted}>
            <div className="course-icon">{isCompleted ? "✓" : "⨉"}</div>
            <span className="course-copy">
                <strong>{course.code}</strong>
                <span>{course.name}</span>
            </span>
            <span className="course-credits">{course.credits} credits</span>
        </button>
    );
}

function CourseModal({ course, onClose }) {
    const assessments = [
        { name: "Assignment 1", grade: "80%", weight: "12%" },
        { name: "Assignment 2", grade: "78%", weight: "12%" },
        { name: "Assignment 3", grade: "88%", weight: "16%" },
        { name: "Midterm", grade: "79%", weight: "25%" },
        { name: "Final Exam", grade: "85%", weight: "35%" },
    ];

    return (
        <div className="modal-backdrop">
            <section className="course-modal">
                <button className="modal-close" onClick={onClose}>x</button>
                <div className="modal-tags">
                    <span>{course.code}</span>
                    <span>{course.credits}</span>
                    <span className="final-tag">Final</span>
                </div>

                <h2>{course.name}</h2>
                <p className="modal-description">Continuation of EECS 1022...</p>
                <div className="modal-summary-grid">
                    <div>
                        <span>Final Grade</span>
                        <strong>85%</strong>
                    </div>
                    <div>
                        <span>Weight Tracked</span>
                        <strong>100%</strong>
                        <p>of 100% total course weight</p>
                    </div>
                </div>

                <h3>Assessments</h3>
                <div className="assessment-table">
                    <div className="assessment-row assessment-head">
                        <span>Name</span>
                        <span>Grade</span>
                        <span>Weight</span>
                    </div>
                    {assessments.map((item) => (
                        <div className="assessment-row" key={item.name}>
                            <span>{item.name}</span>
                            <span>{item.grade}</span>
                            <span>{item.weight}</span>
                        </div>
                    ))}
                </div>

                <p className="modal-note">Read-only view. Editng is not enabled.</p>
            </section>
        </div>
    );
}

// function UsefulLinks() {
//     const links = [
//         ["Connect with an advisor", "https://lassonde.yorku.ca/student-life/connect-with-an-academic-advisor"],
//         ["GPA calculator", "https://students.yorku.ca/york-gpa-calculator"],
//         ["Online services", "https://students.yorku.ca/myonlineservices"],
//         ["Co-op", "https://lassonde.yorku.ca/co-op/"],
//         ["Degree change", "https://myacademicrecord.students.yorku.ca/program-change"],
//         ["Awards & scholarships", "https://students.yorku.ca/sfs/scholarships-awards-bursaries"],
//     ];

//     return (
//         <section className="useful-links-card">
//             <h2>Useful Links</h2>
//             <div className="useful-links-grid">
//                 {links.map(({ label, href }) => (
//                     <a key={label} href={href}>
//                         <span className="link-icon">□</span>
//                         {label}
//                     </a>
//                 ))}
//             </div>
//         </section>
//     );
// }

function formatTitle(key) {
    return key.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function getProgressColorClass(percent) {
    if (percent >= 80) return "progress-green";
    if (percent >= 50) return "progress-orange";
    return "progress-red";
}

function getProgressLabel(percent) {
    if (percent >= 80) return "Almost complete";
    if (percent >= 50) return "In progress";
    return "Just started";
}