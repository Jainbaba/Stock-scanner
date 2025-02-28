import { Box, Paper, Typography, Alert, Tooltip, IconButton } from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

interface NewStocks {
  current_yearweek: string;
  previous_yearweek: string;
  new_symbols_count: number;
  new_symbols: string[];
}

interface NewStocksViewProps {
  newStocks: NewStocks | null;
  handleCopy: (text: string) => void;
}

const NewStocksView: React.FC<NewStocksViewProps> = ({ newStocks, handleCopy }) => {
  if (newStocks === null) {
    return (
      <Alert severity="info" sx={{ backgroundColor: 'primary.light', color: 'primary.contrastText' }}>
        No previous week data available for comparison. Check back next week for new stock additions!
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        New Stocks This Week
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Comparing week {newStocks.current_yearweek} with {newStocks.previous_yearweek}
      </Typography>
      <Typography variant="body1" gutterBottom>
        New Additions: {newStocks.new_symbols_count}
      </Typography>
      <Paper sx={{ p: 2, transition: 'all 0.3s ease-in-out', '&:hover': { boxShadow: 6, transform: 'translateY(-2px)' } }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', maxHeight: '100px', overflow: 'hidden' }}>
          <Typography variant="body2" sx={{ whiteSpace: 'normal', overflow: 'hidden', textOverflow: 'ellipsis', width: '100%' }}>
            {newStocks.new_symbols.join(', ')}
          </Typography>
          <Box flexShrink={0}>
            <Tooltip title="Copy to clipboard">
              <IconButton onClick={() => handleCopy(newStocks.new_symbols.join(', '))}>
                <ContentCopyIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default NewStocksView; 