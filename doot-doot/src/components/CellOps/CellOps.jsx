import { Container, Row } from 'react-bootstrap';
import AddRemoveTrainOp from './AddRemoveTrainOp';
import PlaceOp from './PlaceOp';
import SwitchOp from './SwitchOp';
import RotateOp from './RotateOp';

const CellOps = ({ room, cell }) => (
  <Container>
    <h4>
      Cell Operations
    </h4>
    <Row className="my-2">
      <PlaceOp room={room} cell={cell} />
    </Row>
    {(cell.type === '4' || cell.type === '3' || cell.type === '5')
      && (
      <Row className="my-2">
        <SwitchOp room={room} cell={cell} />
      </Row>
      )}
    <Row className="my-2">
      <RotateOp room={room} cell={cell} />
    </Row>
    {
      cell.type === '8' && (
      <Row className="my-2">
        <AddRemoveTrainOp room={room} cell={cell} />
      </Row>
      )
    }
  </Container>
);

export default CellOps;
