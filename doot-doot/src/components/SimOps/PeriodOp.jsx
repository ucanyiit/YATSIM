import { Button, Slider, Typography } from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../../utils/RequestHandler';

const PeriodOp = ({ room, period: simPeriod = 1.0 }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [period, setPeriod] = useState(parseFloat(simPeriod));

  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        {`Change Period - ${simPeriod}`}
      </Typography>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/period/`, 'post', { period })
            .then()
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <Slider
          marks
          value={period}
          onChange={(e) => { setPeriod(e.target.value); }}
          min={0.5}
          max={4}
          step={0.5}
          valueLabelDisplay="auto"
        />
        {failed && (
        <p>
          Failed request.
        </p>
        )}
        <Button loading={loading} disabled={loading} variant="contained" type="submit">
          Change
        </Button>
      </form>
    </div>
  );
};

export default PeriodOp;
