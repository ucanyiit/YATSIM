/* eslint-disable react/jsx-props-no-spreading */
import { Popover, Typography } from '@mui/material';
import { useState } from 'react';
import CellOps from '../components/CellOps/CellOps';
import GuestOps from '../components/GuestOps/GuestOps';
import SimOps from '../components/SimOps/SimOps';
import './room.css';
import { getCellImage, getWagonImage } from './RoomHelper';

const Popup = ({ sim, cell, room }) => {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ height: '64px' }}>
      <Popover
        anchorOrigin={{
          vertical: 'center',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'center',
          horizontal: 'center',
        }}
        open={open}
        onClose={() => setOpen(false)}
      >
        <div style={{ padding: '1.5rem' }}>
          <CellOps cell={cell} room={room} />
        </div>
      </Popover>
      <button type="button" className="cell-button" onClick={() => setOpen(!open)}>
        <div className="cell">
          <img
            alt="doot"
            className={`direction${cell.direction}`}
            width="64"
            height="64"
            src={getCellImage(cell.type, cell.state)}
          />
          {sim.alive && cell.wagons.map((wagon) => (
            <img
              key={`${wagon.type}`}
              alt="doot-doot"
              className={`train direction${wagon.direction}`}
              width="48"
              height="48"
              src={getWagonImage(wagon.type)}
            />
          ))}
        </div>
      </button>
    </div>
  );
};

const Room = ({
  roomData: {
    room, cells, trains, users, sim,
  }, goHome, user,
}) => {
  const grid = [];
  const newCells = cells.sort((a, b) => {
    if (a.y < b.y) return -1;
    if (a.y > b.y) return 1;
    return a.x < b.x ? -1 : 1;
  });

  // eslint-disable-next-line no-restricted-syntax
  for (let i = 0; i < room.height; i += 1) {
    const row = [];
    for (let j = 0; j < room.width; j += 1) {
      row.push({ ...newCells[i * room.width + j], wagons: [] });
    }
    grid.push(row);
  }

  // eslint-disable-next-line no-restricted-syntax
  for (const train of trains) {
    // eslint-disable-next-line no-restricted-syntax
    for (const wagon of train.wagon_set) {
      grid[wagon.y][wagon.x].wagons.push({ type: train.type, direction: wagon.direction });
    }
    grid[train.source.y][train.source.x].train = train;
  }

  return (
    <div>
      <Typography mt={3} mb={1} variant="h5" component="h1">
        {`${room.id}: `}
        <b>{room.owner.username}</b>
        {`/${room.room_name}, height: ${room.height}, width: ${room.width}, `}
        {sim.running && 'Simulation is running 🚀'}
        {!sim.running && 'Simulation is stopped 🌱'}
      </Typography>
      <Typography variant="subtitle2" component="h2">
        Guests:
        {room.guests.map((u) => (
          <span key={u}>
            {`${u.username}, `}
          </span>
        ))}
        {room.guests.length === 0 && (
        <span>
          {' No guests :('}
        </span>
        )}
      </Typography>
      <center>
        <table cellSpacing="0">
          <tbody>
            {grid.map((row) => (
              <tr key={row[0].y}>
                {row.map((cell) => (
                  <td key={cell.x} className="cell">
                    <Popup sim={sim} cell={cell} room={room} />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </center>
      <SimOps room={room} alive={sim.alive} running={sim.running} period={sim.period} />
      <GuestOps room={room} users={users} goHome={goHome} user={user} />
    </div>
  );
};

export default Room;
