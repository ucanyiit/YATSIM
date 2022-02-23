import {
  Button, FormGroup, MenuItem, Select, Typography,
} from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../../utils/RequestHandler';

const types = [
  { value: '0', name: 'Blank' },
  { value: '1', name: 'Straight' },
  { value: '2', name: 'Curved' },
  { value: '3', name: 'Y Junction' },
  { value: '4', name: 'Y Junction Mirrored' },
  { value: '5', name: 'X Junction' },
  { value: '6', name: 'Cross Roads' },
  { value: '7', name: 'Cross Bridge' },
  { value: '8', name: 'Station' },
];

const PlaceOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [type, setType] = useState(cell.type);

  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        Place
      </Typography>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/place/`, 'post', { x: cell.x, y: cell.y, type })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <FormGroup sx={{ mb: 2 }}>
          <Select
            size="small"
            label="Type"
            value={type}
            onChange={(e) => setType(e.target.value)}
            required
          >
            {types.map((cell_type) => (
              <MenuItem key={cell_type.value} value={cell_type.value}>
                {cell_type.name}
              </MenuItem>
            ))}
          </Select>
        </FormGroup>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button size="small" loading={loading} disabled={loading} variant="contained" type="submit">Place</Button>
      </form>
    </div>
  );
};

export default PlaceOp;
