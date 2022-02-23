import { Grid, Typography } from '@mui/material';
import AddRemoveTrainOp from './AddRemoveTrainOp';
import PlaceOp from './PlaceOp';
import SwitchOp from './SwitchOp';
import RotateOp from './RotateOp';

const CellOps = ({ room, cell }) => (
  <div style={{ minWidth: '35vw' }}>
    <Typography variant="h6" component="h6">
      Cell Operations
    </Typography>
    <Grid
      container
      spacing={2}
      direction="row"
    >
      <Grid item xs={12} md={6}>
        <PlaceOp room={room} cell={cell} />
      </Grid>
      <Grid item xs={12} md={6}>
        <RotateOp room={room} cell={cell} />
      </Grid>
      {cell.type === '8' && (
        <Grid item xs={12} md={6}>
          <AddRemoveTrainOp room={room} cell={cell} />
        </Grid>
      )}
      {(cell.type === '4' || cell.type === '3' || cell.type === '5') && (
      <Grid item xs={12} md={6}>
        <SwitchOp room={room} cell={cell} />
      </Grid>
      )}
    </Grid>
  </div>
);

export default CellOps;
