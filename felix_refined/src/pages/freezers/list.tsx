import {
  Card,
  Col,
  Row,
  Typography,
  Input,
  Button,
  Progress,
  Table,
} from "antd";

const { Title, Text } = Typography;

export const FreezerList = () => {
  const freezerData = [
    {
      key: "1",
      freezer: "Freezer A",
      occupancy: 78,
      freeBoxes: 12,
    },
    {
      key: "2",
      freezer: "Freezer B",
      occupancy: 52,
      freeBoxes: 34,
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Title level={2}>Freezer Inventory</Title>

      {/* TOP SECTION */}
      <Card
        title="Sample Overview"
        style={{ marginBottom: 24 }}
      >
        <Row gutter={24}>
          <Col span={16}>
            <img
              src="https://placehold.co/900x200?text=Sample+Breakdown+Chart"
              alt="Sample breakdown"
              style={{ width: "100%" }}
            />
          </Col>

          <Col span={8}>
            <Text strong>Search Sample Type</Text>

            <Input.Search
              placeholder="e.g. Blood"
              enterButton
              style={{ marginTop: 8 }}
            />

            <div style={{ marginTop: 24 }}>
              <Text>
                Matching samples: --
              </Text>
            </div>
          </Col>
        </Row>
      </Card>

      {/* MIDDLE SECTION */}
      <Card
        title="Freezer Occupation"
        style={{ marginBottom: 24 }}
      >
        <Row gutter={24}>
          <Col span={12}>
            <Table
              pagination={false}
              dataSource={freezerData}
              columns={[
                {
                  title: "Freezer",
                  dataIndex: "freezer",
                },
                {
                  title: "Occupancy",
                  dataIndex: "occupancy",
                  render: (value) => (
                    <Progress percent={value} />
                  ),
                },
                {
                  title: "Free Boxes",
                  dataIndex: "freeBoxes",
                },
              ]}
            />
          </Col>

          <Col span={12}>
            <Text strong>
              Search Boxes With Few Samples
            </Text>

            <Input.Search
              placeholder="e.g. boxes with < 5 samples"
              enterButton
              style={{ marginTop: 8 }}
            />
          </Col>
        </Row>
      </Card>

      {/* BOTTOM SECTION */}
      <Card title="Inventory Actions">
        <Row gutter={16}>
          <Col>
            <Button type="primary">
              Insert Samples
            </Button>
          </Col>

          <Col>
            <Button>
              Move Samples
            </Button>
          </Col>

          <Col>
            <Button danger>
              Outbook Samples
            </Button>
          </Col>
        </Row>
      </Card>
    </div>
  );
};