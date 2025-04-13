import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Tabs,
  Tab,
  Divider,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@material-ui/core';
import { Person, PeopleAlt, Shuffle } from '@material-ui/icons';

import { RootState } from '../../store';
import { ConnectionInfo, ViewMode } from '../../types/family-tree';
import { saveConnectionConsent } from '../../store/actions/familyTree';
import { CoreValuesValidator } from '../ui_components/CoreValuesValidator';

interface ConnectionExplorerProps {
  selectedConnection: ConnectionInfo | null;
  onClose: () => void;
  viewMode: ViewMode;
}

/**
 * ConnectionExplorer - A component for exploring connections in the family tree
 * that embodies the "one and many" philosophy by showing both individual relationship
 * details and how they contribute to the collective pattern.
 */
const ConnectionExplorer: React.FC<ConnectionExplorerProps> = ({
  selectedConnection,
  onClose,
  viewMode
}) => {
  const [activeTab, setActiveTab] = useState(0);
  const [showConsentDialog, setShowConsentDialog] = useState(false);
  const dispatch = useDispatch();
  const currentUser = useSelector((state: RootState) => state.auth.user);

  if (!selectedConnection) return null;

  const isOwnConnection = selectedConnection.source.id === currentUser?.id ||
                         selectedConnection.target.id === currentUser?.id;

  const handleTabChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleUpdateConsent = (newConsent: boolean) => {
    dispatch(saveConnectionConsent({
      connectionId: selectedConnection.id,
      consent: newConsent
    }));
    setShowConsentDialog(false);
  };

  return (
    <Card className="connection-explorer">
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5">Connection Explorer</Typography>
          <Button onClick={onClose} color="primary">Close</Button>
        </Box>

        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          centered
        >
          <Tab
            icon={<Person />}
            label="Individual Relationship"
            aria-label="View individual relationship details"
          />
          <Tab
            icon={<PeopleAlt />}
            label="Collective Impact"
            aria-label="View impact on collective network"
          />
          <Tab
            icon={<Shuffle />}
            label="Perspectives"
            aria-label="View different perspectives on this connection"
          />
        </Tabs>

        <Divider style={{ margin: '16px 0' }} />

        {/* Individual Relationship Tab */}
        {activeTab === 0 && (
          <Box className="individual-relationship-view">
            <Typography variant="h6">
              {selectedConnection.source.name} ↔ {selectedConnection.target.name}
            </Typography>

            <Box display="flex" mt={2} mb={2}>
              <Chip
                label={selectedConnection.type.charAt(0).toUpperCase() +
                       selectedConnection.type.slice(1).replace('_', ' ')}
                color="primary"
              />
              <Chip
                label={`${Math.round(selectedConnection.strength.average * 100)}% strength`}
                variant="outlined"
                style={{ marginLeft: 8 }}
              />
            </Box>

            {isOwnConnection && (
              <Box mt={3}>
                <Typography variant="body2">
                  This connection directly involves you. You have full control over how it's represented.
                </Typography>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => setShowConsentDialog(true)}
                  style={{ marginTop: 8 }}
                >
                  Manage Privacy Settings
                </Button>
              </Box>
            )}

            <CoreValuesValidator
              componentType="relationship-display"
              expectedValues={["sovereignty", "transparency", "consent"]}
              actualImplementation={{
                userHasControl: isOwnConnection,
                dataIsExplainable: true,
                consentIsTracked: true
              }}
            />
          </Box>
        )}

        {/* Collective Impact Tab */}
        {activeTab === 1 && (
          <Box className="collective-impact-view">
            <Typography variant="h6">Contribution to the Whole</Typography>

            <Box mt={2}>
              <Typography variant="body1">
                This connection between {selectedConnection.source.name} and {selectedConnection.target.name} contributes to our collective network in several ways:
              </Typography>

              {selectedConnection.networkImpact && (
                <Box mt={2}>
                  {selectedConnection.networkImpact.bridgingScore > 0.7 && (
                    <Typography variant="body2">
                      • Acts as a <strong>bridge</strong> between otherwise separate communities
                    </Typography>
                  )}
                  {selectedConnection.networkImpact.reinforcementScore > 0.7 && (
                    <Typography variant="body2">
                      • <strong>Reinforces</strong> existing community bonds
                    </Typography>
                  )}
                  {selectedConnection.networkImpact.diversityContribution > 0.7 && (
                    <Typography variant="body2">
                      • Brings <strong>new perspectives</strong> to our community
                    </Typography>
                  )}
                  {selectedConnection.networkImpact.resilienceContribution > 0.7 && (
                    <Typography variant="body2">
                      • Increases our community's <strong>resilience</strong>
                    </Typography>
                  )}
                </Box>
              )}
            </Box>
          </Box>
        )}

        {/* Multiple Perspectives Tab */}
        {activeTab === 2 && (
          <Box className="perspectives-view">
            <Typography variant="h6">Multiple Perspectives</Typography>

            <Box mt={2}>
              <Typography variant="body2">
                How this connection appears from different viewpoints:
              </Typography>

              <Box mt={2}>
                <Typography variant="subtitle2">
                  From {selectedConnection.source.name}'s perspective:
                </Typography>
                <Typography variant="body2">
                  Strength: {Math.round(selectedConnection.strength.sourcePerception * 100)}%
                </Typography>
                {selectedConnection.perspectives?.source && (
                  <Typography variant="body2">
                    "{selectedConnection.perspectives.source}"
                  </Typography>
                )}
              </Box>

              <Box mt={2}>
                <Typography variant="subtitle2">
                  From {selectedConnection.target.name}'s perspective:
                </Typography>
                <Typography variant="body2">
                  Strength: {Math.round(selectedConnection.strength.targetPerception * 100)}%
                </Typography>
                {selectedConnection.perspectives?.target && (
                  <Typography variant="body2">
                    "{selectedConnection.perspectives.target}"
                  </Typography>
                )}
              </Box>

              {viewMode === 'unity' && (
                <Box mt={2}>
                  <Typography variant="subtitle2">
                    From the collective perspective:
                  </Typography>
                  <Typography variant="body2">
                    This connection represents one strand in our interconnected web,
                    contributing to the emergent pattern of our collective experience.
                  </Typography>
                </Box>
              )}
            </Box>
          </Box>
        )}
      </CardContent>

      {/* Consent Management Dialog */}
      <Dialog
        open={showConsentDialog}
        onClose={() => setShowConsentDialog(false)}
        aria-labelledby="consent-dialog-title"
      >
        <DialogTitle id="consent-dialog-title">
          Manage Connection Privacy
        </DialogTitle>
        <DialogContent>
          <Typography>
            You control how this connection is displayed to others.
            Your choice affects only your side of the relationship.
          </Typography>
          <Box mt={2}>
            <Typography variant="subtitle2">Current visibility:</Typography>
            <Typography>
              {selectedConnection.privacySettings?.visibilityLevel || "Default (Community Only)"}
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowConsentDialog(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={() => handleUpdateConsent(false)} color="secondary">
            Hide Connection
          </Button>
          <Button onClick={() => handleUpdateConsent(true)} color="primary">
            Show Connection
          </Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
};

export default ConnectionExplorer;
