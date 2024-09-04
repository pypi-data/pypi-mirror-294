import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from vitalDSP.filtering.signal_filtering import SignalFiltering  # Assuming the filtering functions are implemented
from vitalDSP.visualization.filtering_visualization import FilteringVisualization  # Assuming this is the location of the class

@pytest.fixture
def mock_signal():
    """Fixture for creating a mock signal."""
    return np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.1, 100)

@pytest.fixture
def mock_visualization(mock_signal):
    """Fixture for initializing FilteringVisualization with a mock signal."""
    return FilteringVisualization(mock_signal)

@pytest.fixture
def mock_filtering(mock_visualization):
    """Fixture for mocking the filtering methods."""
    mock_visualization.filtering = MagicMock(SignalFiltering)
    
    # Return a valid numpy array for each mock filter
    filtered_signal = np.sin(np.linspace(0, 10, 100))  # Example filtered signal
    
    mock_visualization.filtering.moving_average.return_value = filtered_signal
    mock_visualization.filtering.gaussian.return_value = filtered_signal
    mock_visualization.filtering.butterworth.return_value = filtered_signal
    mock_visualization.filtering.median.return_value = filtered_signal
    
    return mock_visualization

@patch("plotly.graph_objs.Figure.show")
def test_visualize_moving_average(mock_show, mock_filtering):
    """Test visualize_moving_average method."""
    mock_filtering.visualize_moving_average(window_size=5)
    mock_filtering.filtering.moving_average.assert_called_once_with(5)
    assert mock_show.called

@patch("plotly.graph_objs.Figure.show")
def test_visualize_gaussian_filter(mock_show, mock_filtering):
    """Test visualize_gaussian_filter method."""
    mock_filtering.visualize_gaussian_filter(sigma=1.0)
    mock_filtering.filtering.gaussian.assert_called_once_with(1.0)
    assert mock_show.called

@patch("plotly.graph_objs.Figure.show")
def test_visualize_butterworth_filter(mock_show, mock_filtering):
    """Test visualize_butterworth_filter method."""
    mock_filtering.visualize_butterworth_filter(cutoff=0.3, order=2, fs=100)
    mock_filtering.filtering.butterworth.assert_called_once_with(0.3, 2, 100)
    assert mock_show.called

@patch("plotly.graph_objs.Figure.show")
def test_visualize_median_filter(mock_show, mock_filtering):
    """Test visualize_median_filter method."""
    mock_filtering.visualize_median_filter(kernel_size=5)
    mock_filtering.filtering.median.assert_called_once_with(5)
    assert mock_show.called

@patch("plotly.graph_objs.Figure.show")
def test_visualize_all_filters(mock_show, mock_filtering):
    """Test visualize_all_filters method."""
    mock_filtering.visualize_all_filters(
        window_size=5, sigma=1.0, cutoff=0.5, order=2, fs=1000, kernel_size=5
    )
    
    mock_filtering.filtering.moving_average.assert_called_once_with(5)
    mock_filtering.filtering.gaussian.assert_called_once_with(1.0)
    mock_filtering.filtering.butterworth.assert_called_once_with(0.5, 2, 1000)
    mock_filtering.filtering.median.assert_called_once_with(5)
    
    assert mock_show.called

@patch("plotly.graph_objs.Figure.show")
def test_plot_signal(mock_show, mock_filtering):
    """Test internal _plot_signal method."""
    filtered_signal = np.sin(np.linspace(0, 10, 100))  # Mock filtered signal
    mock_filtering._plot_signal(filtered_signal, title="Test Title")
    assert mock_show.called
