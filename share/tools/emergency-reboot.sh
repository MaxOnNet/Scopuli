#!/usr/bin/env bash
echo "Emergency reboot";
sync;
echo b > /proc/sysrq-trigger;
