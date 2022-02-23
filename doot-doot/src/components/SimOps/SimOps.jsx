import { Container, Grid, Typography } from '@mui/material';
import StartOp from './StartOp';
import StopOp from './StopOp';
import ToggleOp from './ToggleOp';
import PeriodOp from './PeriodOp';

const SimOps = ({
  room, alive, period, running,
}) => (
  <Container>
    <Typography mt={2} variant="h5" component="h5">
      Simulation Operations
    </Typography>
    <Grid
      container
      spacing={2}
      direction="row"
    >
      {!alive && (
        <Grid item xs={6} md={3}>
          <StartOp room={room} />
        </Grid>
      )}
      {alive && (
        <>
          <Grid item xs={6} md={3}>
            <PeriodOp room={room} period={period} />
          </Grid>
          <Grid item xs={6} md={3}>
            <StopOp room={room} />
          </Grid>
          <Grid item xs={6} md={3}>
            <ToggleOp room={room} running={running} />
          </Grid>
        </>
      )}
    </Grid>
  </Container>

);

export default SimOps;
