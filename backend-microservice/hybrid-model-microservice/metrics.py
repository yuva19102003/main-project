from prometheus_client import Summary, Counter, Histogram

# Request processing time
request_processing_time = Summary('request_processing_time_seconds', 'Total time taken to process a request')

# Failed requests counter
failed_requests = Counter('failed_requests', 'Number of failed prediction requests')

# Model-specific prediction counters
efficientnet_predictions = Counter('efficientnet_predictions', 'Count of predictions made by EfficientNet', ['class'])
resnet_predictions = Counter('resnet_predictions', 'Count of predictions made by ResNet', ['class'])
densenet_predictions = Counter('densenet_predictions', 'Count of predictions made by DenseNet', ['class'])

# Model error counter
model_errors = Counter('model_errors', 'Number of incorrect predictions per model', ['model'])

# Image size histogram
image_size_histogram = Histogram('image_size', 'Distribution of input image sizes', buckets=[100, 200, 300, 400, 500])
