import { Container, Row } from 'react-bootstrap';
import PlaceOp from './PlaceOp';
import RotateOp from './RotateOp';
import SwitchOp from './SwitchOp';

const CellOps = ({ room, cell }) => (
  <Container>
    <h4>
      Cell Operations
    </h4>
    <Row className="mb-4">
      <PlaceOp room={room} cell={cell} />
    </Row>
    {(cell.type === '4' || cell.type === '3' || cell.type === '5')
      && (
      <Row className="mb-4">
        <SwitchOp room={room} cell={cell} />
      </Row>
      )}
    <Row>
      <RotateOp room={room} cell={cell} />
    </Row>
  </Container>
);

export default CellOps;
