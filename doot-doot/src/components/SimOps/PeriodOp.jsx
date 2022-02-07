import { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import RequestHandler from '../../utils/RequestHandler';

const PeriodOp = ({ room, period: simPeriod = 1.0 }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [period, setPeriod] = useState(parseFloat(simPeriod));

  return (
    <div>
      <p className="lead">
        Period
      </p>

      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/period/`, 'post', { period })
            .then()
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <p>
          {`Current Period - ${simPeriod}`}
        </p>
        <Form.Label>{`Set Period - ${period}`}</Form.Label>
        <Form.Range
          value={period}
          onChange={(e) => { setPeriod(e.target.value); }}
          min="0.5"
          max="4"
          step="0.5"
        />
        {' '}
        {failed && (
        <p>
          Failed request.
        </p>
        )}
        <Button loading={loading} disabled={loading} variant="primary" type="submit">
          Change Period
        </Button>
      </Form>
    </div>
  );
};

export default PeriodOp;
