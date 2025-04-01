import React from 'react';
import { render } from '@testing-library/react';
import NarrativeComponent from '../../frontend/components/narrative/NarrativeComponent';

test('renders Narrative Mode heading', () => {
  const { getByText } = render(<NarrativeComponent />);
  const headingElement = getByText(/Narrative Mode/i);
  expect(headingElement).toBeInTheDocument();
});
