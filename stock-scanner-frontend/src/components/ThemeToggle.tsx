import React from 'react';
import { IconButton } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

interface ThemeToggleProps {
  mode: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ mode, toggleTheme }) => {
  return (
    <IconButton onClick={toggleTheme} color="inherit">
      {mode === 'light' ? <Brightness4Icon /> : <Brightness7Icon />}
    </IconButton>
  );
};

export default ThemeToggle; 