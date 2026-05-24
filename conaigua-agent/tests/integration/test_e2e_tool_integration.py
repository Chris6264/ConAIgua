from unittest.mock import patch
from conaigua.eda_agent.tools.e2e_pipeline_tool import e2e_pipeline_tool


def test_e2e_tool_calls_runner():
    fake = {
        "result": {
            "station_id": "25019",
            "registros": 365,
            "resumen": {"precip_media": 2.2}
        }
    }

    with patch(
        "conaigua.eda_agent.tools.e2e_pipeline_tool.E2EPipelineRunner.run",
        return_value=fake
    ) as mock_run:

        result = e2e_pipeline_tool.invoke({
            "station_id": "25019"
        })

    mock_run.assert_called_once()
    assert result["station_id"] == "25019"