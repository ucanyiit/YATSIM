import { Container, Row } from 'react-bootstrap';
import StartOp from './StartOp';
import StopOp from './StopOp';
import ToggleOp from './ToggleOp';
import PeriodOp from './PeriodOp';

const SimOps = ({
  room, alive, period, running,
}) => (
  <Container>
    <h4>
      Simulation Operations
    </h4>
    {!alive && (
    <Row className="my-2">
      <StartOp room={room} />
    </Row>
    )}
    {alive && (
    <Row className="my-2">
      <StopOp room={room} />
    </Row>
    )}
    {alive && (
    <Row className="my-2">
      <ToggleOp room={room} running={running} />
    </Row>
    )}
    {alive && (
    <Row className="my-2">
      <PeriodOp room={room} period={period} />
    </Row>
    )}
  </Container>
);

export default SimOps;
