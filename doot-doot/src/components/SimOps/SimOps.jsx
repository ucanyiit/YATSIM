import { Container, Row } from 'react-bootstrap';
import StartOp from './StartOp';
import StopOp from './StopOp';
import ToggleOp from './ToggleOp';

const SimOps = ({ room }) => (
  <Container>
    <h4>
      Simulation Operations
    </h4>
    <Row className="my-2">
      <StartOp room={room} />
    </Row>
    <Row className="my-2">
      <StopOp room={room} />
    </Row>
    <Row className="my-2">
      <ToggleOp room={room} />
    </Row>
  </Container>
);

export default SimOps;
