import {
  Button, FormGroup, MenuItem, Select, Typography,
} from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../../utils/RequestHandler';

const directions = [
  { value: '0', name: 'NORTH' },
  { value: '1', name: 'EAST' },
  { value: '2', name: 'SOUTH' },
  { value: '3', name: 'WEST' },
];

const RotateOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [direction, setDirection] = useState(cell.direction);

  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        Rotate
      </Typography>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/rotate/`, 'post', { x: cell.x, y: cell.y, direction })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <FormGroup sx={{ mb: 2 }}>
          <Select
            size="small"
            label="Direction"
            value={direction}
            onChange={(e) => setDirection(e.target.value)}
            required
          >
            {directions.map((cell_direction) => (
              <MenuItem key={cell_direction.value} value={cell_direction.value}>
                {cell_direction.name}
              </MenuItem>
            ))}
          </Select>
        </FormGroup>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button size="small" loading={loading} disabled={loading} variant="contained" type="submit">Rotate</Button>
      </form>
    </div>
  );
};

export default RotateOp;
