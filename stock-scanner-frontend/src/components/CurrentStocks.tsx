import { Box, Paper, Stack, Typography, IconButton, Tooltip } from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import { formatDate } from '@/services/util';

interface CurrentStocks {
  yearweek: string;
  created_date: string;
  count: number;
  formatted_symbols: string[];
}

interface CurrentStocksProps {
  currentStocks: CurrentStocks;
  handleCopy: (text: string) => void;
}

const CurrentStocksView: React.FC<CurrentStocksProps> = ({ currentStocks, handleCopy }) => {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Current Week Stocks
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Week: {currentStocks.yearweek} ({formatDate(currentStocks.created_date)})
      </Typography>
      <Typography variant="body1" gutterBottom>
        Total Stocks: {currentStocks.count}
      </Typography>
      <Stack spacing={2}>
        {currentStocks.formatted_symbols.length > 0 ? (
          currentStocks.formatted_symbols.map((symbolGroup, index) => (
            <Paper key={index} sx={{ p: 2, transition: 'all 0.3s ease-in-out', '&:hover': { boxShadow: 6, transform: 'translateY(-2px)' } }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', maxHeight: '100px', overflow: 'hidden' }}>
                <Typography variant="body2" sx={{ whiteSpace: 'normal', overflow: 'hidden', textOverflow: 'ellipsis', width: '100%' }}>
                  {symbolGroup}
                </Typography>
                <Box flexShrink={0}>
                  <Tooltip title="Copy to clipboard">
                    <IconButton onClick={() => handleCopy(symbolGroup)}>
                      <ContentCopyIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>
            </Paper>
          ))
        ) : (
          <Typography variant="body2" color="text.secondary">
            No stocks available for this week.
          </Typography>
        )}
      </Stack>
    </Box>
  );
};

export default CurrentStocksView; 