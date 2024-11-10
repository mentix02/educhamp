import Alert from "react-bootstrap/Alert";
import { useState, useEffect, useRef, FormEvent } from "react";

import { submitSurvey } from "./api/survey.ts";
import Navigation from "./components/Navigation.tsx";
import ResultModal from "./components/ResultModal.tsx";
import { InsightResponse } from "./api/types/survey.ts";

export default function App() {
  const [error, setError] = useState<string>();
  const [insight, setInsight] = useState<InsightResponse>();

  const [username, setUsername] = useState<string>("");
  const [questions, setQuestions] = useState<string[]>(new Array(10).fill(""));
  const usernameInputEl = useRef<HTMLInputElement>(null);

  useEffect(() => usernameInputEl.current?.focus(), []);

  const closeModal = () => setInsight(undefined);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setInsight(undefined);
    try {
      const resp = await submitSurvey(username, questions);
      setInsight(resp);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const generateRandomValues = () => {
    const randomUsername = Math.random()
      .toString(36)
      .substring(2, 15 + Math.floor(Math.random() * 10));
    const randomValues = new Array(10).fill(0).map(() => Math.floor(Math.random() * 7) + 1);

    setUsername(randomUsername);
    setQuestions(randomValues.map((value) => value.toString()));
  };

  return (
    <>
      <ResultModal user_id={username} onHide={closeModal} insight={insight} />
      <Navigation />
      <br />
      <div className="container">
        {error && (
          <Alert dismissible variant="danger" onClose={() => setError(undefined)}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="row">
          <div className="col-12 col-lg-4 offset-lg-4">
            <div className="form-floating mb-3">
              <input
                required
                autoFocus
                type="text"
                id="username"
                autoComplete="off"
                value={username}
                ref={usernameInputEl}
                placeholder="Username"
                className="form-control"
                onChange={(e) => setUsername(e.target.value)}
              />
              <label htmlFor="username">Username</label>
            </div>
          </div>
          {questions.map((number, index) => (
            <div className="col-12 col-lg-4 offset-lg-4" key={index}>
              <div className="form-floating mb-3">
                <input
                  required
                  value={number}
                  className="form-control"
                  id={`question${index + 1}`}
                  placeholder={`Question ${index + 1}`}
                  onChange={(event) => {
                    const value = parseInt(event.target.value, 10);
                    if (
                      (isNaN(value) || event.target.value.toLowerCase().includes("e") || value <= 0 || value > 7) &&
                      event.target.value !== ""
                    )
                      return false;
                    setQuestions((questions) =>
                      questions.map((question, i) => (i === index ? event.target.value : question)),
                    );
                  }}
                />
                <label htmlFor={`question${index + 1}`}>Question {index + 1}</label>
              </div>
            </div>
          ))}
          <div className="col-12 col-lg-4 offset-lg-4">
            <div className="d-grid gap-2">
              <button type="submit" className="btn btn-primary">
                Submit
              </button>
              <button type="button" className="btn btn-secondary" onClick={generateRandomValues}>
                Generate Random
              </button>
            </div>
          </div>
        </form>
      </div>
    </>
  );
}
