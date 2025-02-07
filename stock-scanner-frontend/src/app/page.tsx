'use client';
import { useEffect, useState } from 'react';
import { getCurrentStocks, getNewStocks, getLogs } from '@/services/api';
import type { Stock, NewStocks, Log } from '@/services/api';
import { 
  Container, 
  Tabs, 
  Tab, 
  Box,
  Typography,
  Button,
  Stack,
  Link
} from '@mui/material';
import { Loading } from '@/components/ui/loading';
import { ErrorMessage } from '@/components/ui/error';

export default function Home() {
  const [currentStocks, setCurrentStocks] = useState<Stock | null>(null);
  const [newStocks, setNewStocks] = useState<NewStocks | null>(null);
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

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

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Stack spacing={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Stock Scanner
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Current Stocks" />
            <Tab label="New Stocks" />
            <Tab label="Logs" />
          </Tabs>
        </Box>

        <Box role="tabpanel" hidden={tabValue !== 0}>
          {tabValue === 0 && (
            <Box>
              {/* Add your current stocks content here */}
              <pre>{JSON.stringify(currentStocks, null, 2)}</pre>
            </Box>
          )}
        </Box>

        <Box role="tabpanel" hidden={tabValue !== 1}>
          {tabValue === 1 && (
            <Box>
              {/* Add your new stocks content here */}
              <pre>{JSON.stringify(newStocks, null, 2)}</pre>
            </Box>
          )}
        </Box>

        <Box role="tabpanel" hidden={tabValue !== 2}>
          {tabValue === 2 && (
            <Box>
              {/* Add your logs content here */}
              <pre>{JSON.stringify(logs, null, 2)}</pre>
            </Box>
          )}
        </Box>

        <Stack direction="row" spacing={2} justifyContent="center">
          <Button 
            variant="contained" 
            component={Link}
            href="https://vercel.com/new"
            target="_blank"
            rel="noopener noreferrer"
          >
            Deploy Now
          </Button>
          <Button 
            variant="outlined"
            component={Link}
            href="https://nextjs.org/docs"
            target="_blank"
            rel="noopener noreferrer"
          >
            Read Docs
          </Button>
        </Stack>
      </Stack>
    </Container>
  );
}
