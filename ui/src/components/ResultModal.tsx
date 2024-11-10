import { useState, useEffect } from "react";
import Modal from "react-bootstrap/Modal";
import Table from "react-bootstrap/Table";

import { fetchStats } from "../api/survey.ts";
import { StatsResponse, InsightResponse } from "../api/types/survey.ts";

type ResultModalProps = {
  user_id: string;
  onHide: () => void;
  insight?: InsightResponse;
};

export default function ResultModal({ onHide, insight, user_id }: ResultModalProps) {
  const [stats, setStats] = useState<StatsResponse>();
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!insight) return;
    fetchStats(user_id)
      .then(setStats)
      .catch((err) => alert(err.message))
      .finally(() => setLoading(false));
  }, [insight]);

  return (
    <Modal size="lg" show={insight !== undefined} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Survey Insights</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Table striped hover>
          <tbody>
            <tr>
              <td>Fur Value</td>
              <td>{insight?.fur_value}</td>
            </tr>
            <tr>
              <td>Tail Value</td>
              <td>{insight?.tail_value}</td>
            </tr>
            <tr>
              <td>Cat/Dog</td>
              <td>{insight?.cat_dog}</td>
            </tr>
            <tr>
              <td>Overall Analysis</td>
              <td>{insight?.overall_analysis}</td>
            </tr>
            <tr>
              <td>Description</td>
              <td>{insight?.description}</td>
            </tr>
            <tr>
              <td>Mean</td>
              <td>{loading ? "Loading..." : stats?.mean}</td>
            </tr>
            <tr>
              <td>Median</td>
              <td>{loading ? "Loading..." : stats?.median}</td>
            </tr>
            <tr>
              <td>Standard Deviation</td>
              <td>{loading ? "Loading..." : stats?.std_dev}</td>
            </tr>
          </tbody>
        </Table>
      </Modal.Body>
    </Modal>
  );
}
