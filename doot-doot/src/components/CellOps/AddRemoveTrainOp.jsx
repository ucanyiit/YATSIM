import {
  Button, FormGroup, MenuItem, Select, TextField, Typography,
} from '@mui/material';
import { useState } from 'react';
import RequestHandler from '../../utils/RequestHandler';

const types = [
  { value: '0', name: 'Mitski' },
  { value: '1', name: 'Lady Gaga' },
];

const AddRemoveTrainOp = ({ room, cell }) => {
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [type, setType] = useState(cell.train?.type || 0);
  const [length, setLength] = useState(1);
  const type_name = cell.train?.type === 1 ? 'Lady Gaga' : 'Mitski';

  if (cell.train) {
    return (
      <div>
        <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
          {`Remove ${type_name}`}
        </Typography>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            setLoading(true);
            (new RequestHandler()).request(`room/${room.id}/train`, 'delete', { train_id: cell.train.id })
              .then(() => {})
              .catch(() => setFailed(true))
              .finally(() => setLoading(false));
          }}
        >
          {failed && (
            <p>
              Failed request.
            </p>
          )}
          <Button size="small" loading={loading} disabled={loading} variant="contained" type="submit">Remove</Button>
        </form>
      </div>
    );
  }
  return (
    <div>
      <Typography variant="subtitle1" component="h6" mt={1} mb={1}>
        Add Train
      </Typography>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          setLoading(true);
          (new RequestHandler()).request(`room/${room.id}/train/`, 'post', { source: { x: cell.x, y: cell.y }, type, length })
            .then(() => {})
            .catch(() => setFailed(true))
            .finally(() => setLoading(false));
        }}
      >
        <FormGroup sx={{ mb: 2 }}>
          <Select sx={{ mb: 2 }} value={type} onChange={(e) => setType(e.target.value)}>
            {types.map((train_type) => (
              <MenuItem key={train_type.value} value={train_type.value}>
                {train_type.name}
              </MenuItem>
            ))}
          </Select>
        </FormGroup>
        <FormGroup sx={{ mb: 2 }}>
          <TextField label="Length" type="number" placeholder="Length" onChange={(e) => setLength(e.target.value)} min={1} max={20} required />
        </FormGroup>
        {failed && (
          <p>
            Failed request.
          </p>
        )}
        <Button size="small" loading={loading} disabled={loading} variant="contained" type="submit">Add</Button>
      </form>
    </div>
  );
};

export default AddRemoveTrainOp;
