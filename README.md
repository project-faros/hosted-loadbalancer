# hosted-loadbalancer
A self hosted load balancer for a Kubernetes cluster

## Introduction

## Architecture

## Installation

## Limitations

1) Currently only works for clusters where the ingress router
   is located on the Masters. This limitation is not planned
   to be permanent.
2) The self hosted load balancer is not actually a load
   balancer at all. It simply moves the external load baalancer's
   VIP to the cluster on a node where the ingress router is
   running. The ingress router then functions as the cluster's
   primary load balancer. This solution is meant for minimal
   edge-style deployments so this limitation should be
   acceptable within those parameters.
3) An external load balancer is still required to boot the
   cluster. The cluster cannot take over load balancing until
   it is fully operational. For this reason, the external load
   balancer must be powered on, then the cluster powered on,
   and then the external load balancer can safely be removed.
