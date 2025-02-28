import { Box, IconButton, Badge, Menu, MenuItem, Typography } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';

import { useState } from 'react';
import { formatDate } from '@/services/util';

interface Log {
  timestamp: string;
  message: string;
}

interface NotificationMenuProps {
  logs: Log[];
}

const NotificationMenu: React.FC<NotificationMenuProps> = ({ logs }) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box>
      <IconButton onClick={handleClick} color="inherit" sx={{ mr: 1 }}>
        <Badge badgeContent={logs.length} color="primary">
          <NotificationsIcon />
        </Badge>
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box sx={{ maxHeight: 200, overflowY: 'auto', width: 300 }}>
          {logs.slice(0, 5).map((log, index) => (
            <MenuItem key={index} onClick={handleClose}>
              <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'normal', overflowWrap: 'break-word', width: '100%' }}>
                {formatDate(log.timestamp)} - {log.message}
              </Typography>
            </MenuItem>
          ))}
        </Box>
      </Menu>
    </Box>
  );
};

export default NotificationMenu; 