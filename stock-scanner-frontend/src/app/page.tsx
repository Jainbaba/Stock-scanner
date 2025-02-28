'use client';
import { useEffect, useState } from 'react';
import { getCurrentStocks, getNewStocks, getLogs } from '@/services/api';
import type { Stock, NewStocks, Log } from '@/services/api';
import { 
  Container, 
  Box,
  Typography,
  Stack,
  ThemeProvider,
  createTheme,
  CssBaseline,
} from '@mui/material';
import { Loading } from '@/components/ui/loading';
import { ErrorMessage } from '@/components/ui/error';
import CurrentStocksView from '@/components/CurrentStocks';
import NewStocksView from '@/components/NewStocks';
import NotificationMenu from '@/components/NotificationMenu';
import ThemeToggle from '@/components/ThemeToggle';

export default function Home() {
  const [currentStocks, setCurrentStocks] = useState<Stock | null>(null);
  const [newStocks, setNewStocks] = useState<NewStocks | null>(null);
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<'light' | 'dark'>('light');
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const theme = createTheme({
    palette: {
      mode,
      primary: {
        main: mode === 'light' ? '#2196f3' : '#90caf9',
      },
      secondary: {
        main: mode === 'light' ? '#f50057' : '#f48fb1',
      },
      background: {
        default: mode === 'light' ? '#f5f5f5' : '#121212',
        paper: mode === 'light' ? '#ffffff' : '#1e1e1e',
      },
    },
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [stocksData, newStocksData, logsData] = await Promise.all([
          getCurrentStocks(),
          getNewStocks(),
          getLogs()
        ]);

        setCurrentStocks(stocksData);
        setNewStocks(newStocksData);
        setLogs(logsData.slice(0, 5));
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const savedMode = localStorage.getItem('theme-mode') as 'light' | 'dark' | null;
    if (savedMode) {
      setMode(savedMode);
    }
  }, []);

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  const toggleTheme = () => {
    const newMode = mode === 'light' ? 'dark' : 'light';
    setMode(newMode);
    localStorage.setItem('theme-mode', newMode);
  };

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  if (loading) return <Loading />;
  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Stack spacing={4}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4" component="h1" gutterBottom>
              Stock Scanner
            </Typography>
            <Box display="flex" alignItems="center">
              <ThemeToggle mode={mode} toggleTheme={toggleTheme} />
              <NotificationMenu logs={logs} />
            </Box>
          </Box>

          <CurrentStocksView 
            currentStocks={currentStocks || { yearweek: '', created_date: '', count: 0, formatted_symbols: [] }} 
            handleCopy={handleCopy} 
          />
          <NewStocksView newStocks={newStocks} handleCopy={handleCopy} />
        </Stack>
      </Container>
    </ThemeProvider>
  );
}
