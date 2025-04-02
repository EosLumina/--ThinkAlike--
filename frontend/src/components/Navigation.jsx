import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Container,
  Avatar,
  Button,
  Tooltip,
  MenuItem,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import {
  Menu as MenuIcon,
  Person,
  LocationOn,
  Event,
  Settings,
  Logout,
  Search,
  Group,
  Dashboard,
  Shield
} from '@mui/icons-material';

const Navigation = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleLogout = () => {
    handleCloseUserMenu();
    logout();
  };

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setDrawerOpen(open);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <>
      <AppBar position="static" color="primary">
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
              onClick={toggleDrawer(true)}
            >
              <MenuIcon />
            </IconButton>
            
            <Typography
              variant="h6"
              noWrap
              component={Link}
              to="/"
              sx={{
                mr: 2,
                display: { xs: 'none', md: 'flex' },
                fontWeight: 700,
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              ThinkAlike
            </Typography>

            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              <Button
                component={Link}
                to="/discover"
                sx={{
                  my: 2,
                  color: 'white',
                  display: 'block',
                  backgroundColor: isActive('/discover') ? 'rgba(255,255,255,0.2)' : 'transparent'
                }}
              >
                Discover
              </Button>
              
              <Button
                component={Link}
                to="/communities"
                sx={{
                  my: 2,
                  color: 'white',
                  display: 'block',
                  backgroundColor: isActive('/communities') ? 'rgba(255,255,255,0.2)' : 'transparent'
                }}
              >
                Communities
              </Button>
              
              <Button
                component={Link}
                to="/location-sharing"
                sx={{
                  my: 2,
                  color: 'white',
                  display: 'block',
                  backgroundColor: isActive('/location-sharing') ? 'rgba(255,255,255,0.2)' : 'transparent'
                }}
              >
                Location
              </Button>
            </Box>

            {isAuthenticated ? (
              <Box sx={{ flexGrow: 0 }}>
                <Tooltip title="Open settings">
                  <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                    <Avatar 
                      alt={user?.username || "User"} 
                      src={user?.profile?.profile_picture_url}
                      sx={{ bgcolor: 'secondary.main' }}
                    >
                      {user?.username?.[0]?.toUpperCase() || "U"}
                    </Avatar>
                  </IconButton>
                </Tooltip>
                <Menu
                  sx={{ mt: '45px' }}
                  id="menu-appbar"
                  anchorEl={anchorElUser}
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorElUser)}
                  onClose={handleCloseUserMenu}
                >
                  <MenuItem component={Link} to="/profile" onClick={handleCloseUserMenu}>
                    <ListItemIcon>
                      <Person fontSize="small" />
                    </ListItemIcon>
                    <ListItemText>Profile</ListItemText>
                  </MenuItem>
                  
                  <MenuItem component={Link} to="/settings" onClick={handleCloseUserMenu}>
                    <ListItemIcon>
                      <Settings fontSize="small" />
                    </ListItemIcon>
                    <ListItemText>Settings</ListItemText>
                  </MenuItem>
                  
                  <Divider />
                  
                  <MenuItem onClick={handleLogout}>
                    <ListItemIcon>
                      <Logout fontSize="small" />
                    </ListItemIcon>
                    <ListItemText>Logout</ListItemText>
                  </MenuItem>
                </Menu>
              </Box>
            ) : (
              <Box sx={{ flexGrow: 0 }}>
                <Button 
                  component={Link} 
                  to="/login" 
                  variant="outlined" 
                  sx={{ color: 'white', borderColor: 'white', mr: 1 }}
                >
                  Login
                </Button>
                <Button 
                  component={Link} 
                  to="/register" 
                  variant="contained" 
                  color="secondary"
                >
                  Sign Up
                </Button>
              </Box>
            )}
          </Toolbar>
        </Container>
      </AppBar>

      {/* Drawer Navigation */}
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer(false)}
      >
        <Box
          sx={{ width: 250 }}
          role="presentation"
          onClick={toggleDrawer(false)}
          onKeyDown={toggleDrawer(false)}
        >
          <List>
            <ListItem>
              <Typography variant="h6" sx={{ fontWeight: 'bold' }}>ThinkAlike</Typography>
            </ListItem>
            
            <Divider />
            
            <ListItem button component={Link} to="/discover">
              <ListItemIcon>
                <Search />
              </ListItemIcon>
              <ListItemText primary="Discover" />
            </ListItem>
            
            <ListItem button component={Link} to="/communities">
              <ListItemIcon>
                <Group />
              </ListItemIcon>
              <ListItemText primary="Communities" />
            </ListItem>
            
            <ListItem button component={Link} to="/events">
              <ListItemIcon>
                <Event />
              </ListItemIcon>
              <ListItemText primary="Events" />
            </ListItem>
            
            <ListItem button component={Link} to="/location-sharing">
              <ListItemIcon>
                <LocationOn />
              </ListItemIcon>
              <ListItemText primary="Location Sharing" />
            </ListItem>
            
            <Divider />
            
            {isAuthenticated && (
              <>
                <ListItem button component={Link} to="/profile">
                  <ListItemIcon>
                    <Person />
                  </ListItemIcon>
                  <ListItemText primary="Profile" />
                </ListItem>
                
                <ListItem button component={Link} to="/settings">
                  <ListItemIcon>
                    <Settings />
                  </ListItemIcon>
                  <ListItemText primary="Settings" />
                </ListItem>
                
                <ListItem button component={Link} to="/dashboard">
                  <ListItemIcon>
                    <Dashboard />
                  </ListItemIcon>
                  <ListItemText primary="Dashboard" />
                </ListItem>
              </>
            )}
            
            <Divider />
            
            <ListItem button component={Link} to="/data-traceability">
              <ListItemIcon>
                <Shield />
              </ListItemIcon>
              <ListItemText primary="Data Traceability" />
            </ListItem>
            
            {isAuthenticated && (
              <ListItem button onClick={handleLogout}>
                <ListItemIcon>
                  <Logout />
                </ListItemIcon>
                <ListItemText primary="Logout" />
              </ListItem>
            )}
          </List>
        </Box>
      </Drawer>
    </>
  );
};

export default Navigation;